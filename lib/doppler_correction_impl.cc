/* -*- c++ -*- */
/*
 * Copyright 2022-2023,2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "doppler_correction_impl.h"
#include <gnuradio/expj.h>
#include <gnuradio/io_signature.h>
#include <spdlog/fmt/fmt.h>
#include <chrono>
#include <fstream>
#include <stdexcept>

namespace gr {
namespace satellites {

doppler_correction::sptr doppler_correction::make(const std::string& filename,
                                                  double samp_rate,
                                                  double t0,
                                                  const std::string& timesync_tag)
{
    return gnuradio::make_block_sptr<doppler_correction_impl>(
        filename, samp_rate, t0, timesync_tag);
}


doppler_correction_impl::doppler_correction_impl(const std::string& filename,
                                                 double samp_rate,
                                                 double t0,
                                                 const std::string& timesync_tag)
    : gr::sync_block("doppler_correction",
                     gr::io_signature::make(1, 1, sizeof(gr_complex)),
                     gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_phase(0.0),
      d_samp_rate(samp_rate),
      d_current_index(0),
      d_t0(t0),
      d_sample_t0(0),
      d_rx_time_key(pmt::mp("rx_time")),
      d_pck_n_key(pmt::mp("pck_n")),
      d_full_key(pmt::mp("full")),
      d_frac_key(pmt::mp("frac")),
      d_timesync_enabled(!timesync_tag.empty()),
      d_timesync_key(pmt::mp(timesync_tag)),
      d_current_time(t0),
      d_current_freq(0.0)
{
    read_doppler_file(filename);
}

doppler_correction_impl::~doppler_correction_impl() {}

void doppler_correction_impl::read_doppler_file(const std::string& filename)
{
    std::ifstream input_file(filename);
    if (!input_file.good()) {
        throw std::runtime_error(
            fmt::format("error opening Doppler file '{}'", filename));
    }
    double time;
    double frequency;

    while (!input_file.eof()) {
        if (!input_file.good()) {
            throw std::runtime_error("format error in Doppler file");
        }
        input_file >> time >> frequency;
        times.push_back(time);
        freqs_rad_per_sample.push_back(2.0 * GR_M_PI * frequency / d_samp_rate);
    }
    if (freqs_rad_per_sample.size() >= 1) {
        d_current_freq = freqs_rad_per_sample[0];
    }
}

void doppler_correction_impl::set_time(double t)
{
    gr::thread::scoped_lock guard(d_setlock);
    d_sample_t0 = nitems_written(0);
    d_t0 = t;
    d_logger->info("set time {} at sample {}", d_t0, d_sample_t0);
    adjust_current_index();
}

int doppler_correction_impl::work(int noutput_items,
                                  gr_vector_const_void_star& input_items,
                                  gr_vector_void_star& output_items)
{
    gr::thread::scoped_lock guard(d_setlock);
    auto in = static_cast<const gr_complex*>(input_items[0]);
    auto out = static_cast<gr_complex*>(output_items[0]);

    std::vector<gr::tag_t> tags;
    get_tags_in_window(tags, 0, 0, noutput_items);
    for (const auto& tag : tags) {
        double t0;
        bool set = false;
        bool log_debug = false;
        if (pmt::eqv(tag.key, d_rx_time_key)) {
            if (pmt::is_tuple(tag.value)) {
                t0 = static_cast<double>(pmt::to_uint64(pmt::tuple_ref(tag.value, 0))) +
                     pmt::to_double(pmt::tuple_ref(tag.value, 1));
                set = true;
            }
        } else if (pmt::eqv(tag.key, d_pck_n_key)) {
            if (pmt::is_dict(tag.value)) {
                const auto full_pmt = pmt::dict_ref(tag.value, d_full_key, pmt::PMT_NIL);
                const auto frac_pmt = pmt::dict_ref(tag.value, d_frac_key, pmt::PMT_NIL);
                if (pmt::is_integer(full_pmt) && pmt::is_uint64(frac_pmt)) {
                    const auto full = pmt::to_long(full_pmt);
                    const auto frac = pmt::to_uint64(frac_pmt);
                    // in DIFI, frac gives the number of picoseconds
                    t0 = static_cast<double>(full) + 1e-12 * static_cast<double>(frac);
                    set = true;
                }
            }
        } else if (d_timesync_enabled && pmt::eqv(tag.key, d_timesync_key)) {
            const auto now = std::chrono::high_resolution_clock::now();
            const std::chrono::duration<double> t_unix = now.time_since_epoch();
            t0 = t_unix.count();
            set = true;
            log_debug = true;
        }

        if (set) {
            d_sample_t0 = tag.offset;
            d_t0 = t0;
            if (log_debug) {
                // use debug logging for timesync tag, since logging once per
                // packet can be too expensive
                d_logger->debug("set time {} at sample {}", d_t0, d_sample_t0);
            } else {
                d_logger->info("set time {} at sample {}", d_t0, d_sample_t0);
            }
            adjust_current_index();
        }
    }

    double time = 0.0;
    double freq = 0.0;
    for (int j = 0; j < noutput_items; ++j) {
        time = d_t0 + static_cast<double>(static_cast<int64_t>(nitems_written(0)) -
                                          static_cast<int64_t>(d_sample_t0) +
                                          static_cast<int64_t>(j)) /
                          d_samp_rate;
        // Advance d_current_index so that the next time is greater than the
        // current.
        while (d_current_index + 1 < times.size() && times[d_current_index + 1] <= time) {
            ++d_current_index;
        }
        if ((time < times[d_current_index]) || (d_current_index + 1 == times.size())) {
            // We are before the beginning or past the end of the file, so we
            // maintain a constant frequency.
            freq = freqs_rad_per_sample[d_current_index];
        } else {
            // Linearly interpolate frequency
            double alpha = (time - times[d_current_index]) /
                           (times[d_current_index + 1] - times[d_current_index]);
            freq = (1.0 - alpha) * freqs_rad_per_sample[d_current_index] +
                   alpha * freqs_rad_per_sample[d_current_index + 1];
        }
        d_phase += freq;
        phase_wrap();
        const gr_complex nco = gr_expj(-static_cast<float>(d_phase));
        gr::fast_cc_multiply(out[j], in[j], nco);
    }

    d_current_freq = freq;
    d_current_time = time;

    return noutput_items;
}

} /* namespace satellites */
} /* namespace gr */
