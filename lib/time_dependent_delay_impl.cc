/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "time_dependent_delay_impl.h"
#include <gnuradio/io_signature.h>
#include <fstream>
#include <stdexcept>

namespace gr {
namespace satellites {

time_dependent_delay::sptr time_dependent_delay::make(const std::string& filename,
                                                      double samp_rate,
                                                      double t0,
                                                      const std::vector<float>& taps,
                                                      int num_filters)
{
    return gnuradio::make_block_sptr<time_dependent_delay_impl>(
        filename, samp_rate, t0, taps, num_filters);
}


time_dependent_delay_impl::time_dependent_delay_impl(const std::string& filename,
                                                     double samp_rate,
                                                     double t0,
                                                     const std::vector<float>& taps,
                                                     int num_filters)
    : gr::sync_block("time_dependent_delay",
                     gr::io_signature::make(1, 1, sizeof(gr_complex)),
                     gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_samp_rate(samp_rate),
      d_current_index(0),
      d_t0(t0),
      d_sample_t0(0),
      d_fir_delay((static_cast<double>(taps.size()) - 1.0) /
                  (2.0 * static_cast<double>(num_filters))),
      d_taps_per_filter((taps.size() + num_filters - 1) / num_filters),
      d_rx_time_key(pmt::mp("rx_time")),
      d_pck_n_key(pmt::mp("pck_n")),
      d_full_key(pmt::mp("full")),
      d_frac_key(pmt::mp("frac")),
      d_current_time(t0),
      d_current_delay(0.0)
{
    for (int nfilt = 0; nfilt < num_filters; ++nfilt) {
        std::vector<float> filt_taps(d_taps_per_filter);
        for (size_t j = 0; j * num_filters + nfilt < taps.size(); ++j) {
            filt_taps[j] = taps[j * num_filters + nfilt];
        }
        d_filters.emplace_back(filt_taps);
    }

    read_delay_file(filename);

    double max_delay = 0.0;
    for (double delay : d_delays_samples) {
        max_delay = std::max(max_delay, delay);
    }

    // part of history due to delays
    const int delay_hist = static_cast<int>(max_delay - d_fir_delay) + 1;
    // part of history due to FIR filter
    const int fir_hist = d_taps_per_filter - 1;
    set_history(delay_hist + fir_hist);

    set_tag_propagation_policy(TPP_DONT);
}

time_dependent_delay_impl::~time_dependent_delay_impl() {}

void time_dependent_delay_impl::read_delay_file(const std::string& filename)
{
    std::ifstream input_file(filename);
    if (!input_file.good()) {
        throw std::runtime_error("error opening delay file");
    }

    while (!input_file.eof()) {
        if (!input_file.good()) {
            throw std::runtime_error("format error in delay file");
        }
        double time;
        double delay_seconds;
        input_file >> time >> delay_seconds;
        const double delay_samples = delay_seconds * d_samp_rate;
        if (delay_samples < d_fir_delay) {
            throw std::runtime_error("delay samples is smaller than FIR group delay");
        }
        d_times.push_back(time);
        d_delays_samples.push_back(delay_samples);
    }
    if (d_delays_samples.size() >= 1) {
        d_current_delay = d_delays_samples[0];
    }
}

void time_dependent_delay_impl::set_time(double t)
{
    gr::thread::scoped_lock guard(d_setlock);
    d_sample_t0 = nitems_written(0);
    d_t0 = t;
    d_logger->info("set time {} at sample {}", d_t0, d_sample_t0);
    adjust_current_index();
}

int time_dependent_delay_impl::work(int noutput_items,
                                    gr_vector_const_void_star& input_items,
                                    gr_vector_void_star& output_items)
{
    gr::thread::scoped_lock guard(d_setlock);
    auto in = static_cast<const gr_complex*>(input_items[0]);
    auto out = static_cast<gr_complex*>(output_items[0]);

    update_time_from_tags(noutput_items);

    const auto _history = history();
    const auto _nitems_written = nitems_written(0);
    double time = 0.0;
    double delay = 0.0;
    for (int j = 0; j < noutput_items; ++j) {
        time = compute_time(_nitems_written + static_cast<uint64_t>(j));
        delay = compute_delay(time);
        const double delay_before_fir = delay - d_fir_delay;
        int delay_int = static_cast<int>(delay_before_fir);
        double advance_frac = 1.0 - (delay_before_fir - delay_int);
        if (advance_frac == 1.0) {
            advance_frac = 0.0;
        } else {
            ++delay_int;
        }
        const int sample_idx0 = j + _history - 1 - delay_int - (d_taps_per_filter - 1);
        const double filter_idx_double =
            advance_frac * static_cast<double>(d_filters.size());
        const int filter_idx0 = static_cast<int>(filter_idx_double);
        int sample_idx1 = sample_idx0;
        int filter_idx1 = filter_idx0 + 1;
        if (filter_idx1 == static_cast<int>(d_filters.size())) {
            ++sample_idx1;
            filter_idx1 = 0;
        }
        const gr_complex z0 = d_filters[filter_idx0].filter(&in[sample_idx0]);
        const gr_complex z1 = d_filters[filter_idx1].filter(&in[sample_idx1]);
        const float filter_idx_frac =
            filter_idx_double - static_cast<double>(filter_idx0);
        out[j] = (1.0f - filter_idx_frac) * z0 + filter_idx_frac * z1;
    }
    d_current_time = time;
    d_current_delay = delay;

    // Propagate tags manually. Place tags which are in the future in
    // d_future_tags to avoid adding tags for items that are not produced yet.
    const uint64_t add_limit = _nitems_written + noutput_items;
    std::vector<gr::tag_t> tags;
    get_tags_in_window(tags, 0, 0, noutput_items);
    for (auto tag : tags) {
        const double tag_delay = compute_tag_delay(compute_time(tag.offset));
        const uint64_t tag_delay_round = static_cast<uint64_t>(std::round(tag_delay));
        // Note: this is an approximation. It assumes that the delay does not
        // change significantly between now and now + tag_delay, which is when
        // the tag will be placed.
        tag.offset += tag_delay_round;
        if (tag.offset < add_limit) {
            add_item_tag(0, tag);
        } else {
            d_future_tags.push_back(std::move(tag));
        }
    }

    // Output tags from previous work() which are not in the future anymore.
    auto tag = d_future_tags.cbegin();
    for (; tag < d_future_tags.cend(); ++tag) {
        if (tag->offset < add_limit) {
            add_item_tag(0, *tag);
        } else {
            break;
        }
    }
    d_future_tags.erase(d_future_tags.begin(), tag);

    return noutput_items;
}

} /* namespace satellites */
} /* namespace gr */
