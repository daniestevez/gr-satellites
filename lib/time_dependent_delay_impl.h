/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_TIME_DEPENDENT_DELAY_IMPL_H
#define INCLUDED_SATELLITES_TIME_DEPENDENT_DELAY_IMPL_H

#include <gnuradio/filter/fir_filter.h>
#include <satellites/time_dependent_delay.h>
#include <cstdint>

namespace gr {
namespace satellites {

class time_dependent_delay_impl : public time_dependent_delay
{
private:
    const double d_samp_rate;
    size_t d_current_index;
    double d_t0;
    uint64_t d_sample_t0;
    std::vector<double> d_times;
    std::vector<double> d_delays_samples; // delays in the file in units of samples
    std::vector<gr::filter::kernel::fir_filter_ccf> d_filters;
    const double d_fir_delay;
    const int d_taps_per_filter;
    std::vector<gr::tag_t> d_future_tags;

    // Used by UHD
    const pmt::pmt_t d_rx_time_key;

    // Used by gr-difi
    const pmt::pmt_t d_pck_n_key;
    const pmt::pmt_t d_full_key;
    const pmt::pmt_t d_frac_key;

    double d_current_time;
    double d_current_delay; // current delay in units of samples

    // Called after a time update. Makes the current index go backwards if
    // needed because of a time update "to the past".
    void adjust_current_index()
    {
        while ((d_current_index > 0) && (d_times[d_current_index] > d_t0)) {
            --d_current_index;
        }
    }

    void read_delay_file(const std::string& filename);

    void update_time_from_tags(int noutput_items)
    {
        std::vector<gr::tag_t> tags;
        get_tags_in_window(tags, 0, 0, noutput_items);
        for (const auto& tag : tags) {
            double t0;
            bool set = false;
            if (pmt::eqv(tag.key, d_rx_time_key)) {
                if (pmt::is_tuple(tag.value)) {
                    t0 = static_cast<double>(
                             pmt::to_uint64(pmt::tuple_ref(tag.value, 0))) +
                         pmt::to_double(pmt::tuple_ref(tag.value, 1));
                    set = true;
                }
            } else if (pmt::eqv(tag.key, d_pck_n_key)) {
                if (pmt::is_dict(tag.value)) {
                    const auto full_pmt =
                        pmt::dict_ref(tag.value, d_full_key, pmt::PMT_NIL);
                    const auto frac_pmt =
                        pmt::dict_ref(tag.value, d_frac_key, pmt::PMT_NIL);
                    if (pmt::is_integer(full_pmt) && pmt::is_uint64(frac_pmt)) {
                        const auto full = pmt::to_long(full_pmt);
                        const auto frac = pmt::to_uint64(frac_pmt);
                        // in DIFI, frac gives the number of picoseconds
                        t0 =
                            static_cast<double>(full) + 1e-12 * static_cast<double>(frac);
                        set = true;
                    }
                }
            }

            if (set) {
                d_sample_t0 = tag.offset;
                d_t0 = t0;
                d_logger->info("set time {} at sample {}", d_t0, d_sample_t0);
                adjust_current_index();
            }
        }
    }

    // this cannot be const, because nitems_written() is not const
    double compute_time(uint64_t sample_absolute_idx) const
    {
        return d_t0 + static_cast<double>(static_cast<int64_t>(sample_absolute_idx) -
                                          static_cast<int64_t>(d_sample_t0)) /
                          d_samp_rate;
    }

    double compute_delay(double time)
    {
        // Advance d_current_index so that the next time is greater than the
        // current.
        while (d_current_index + 1 < d_times.size() &&
               d_times[d_current_index + 1] <= time) {
            ++d_current_index;
        }
        if ((time < d_times[d_current_index]) ||
            (d_current_index + 1 == d_times.size())) {
            // We are before the beginning or past the end of the file, so we
            // maintain a constant delay.
            return d_delays_samples[d_current_index];
        }
        // Linearly interpolate delay
        double alpha = (time - d_times[d_current_index]) /
                       (d_times[d_current_index + 1] - d_times[d_current_index]);
        return (1.0 - alpha) * d_delays_samples[d_current_index] +
               alpha * d_delays_samples[d_current_index + 1];
    }

    // compute delay without touching d_current_index
    double compute_tag_delay(double time) const
    {
        size_t current_index = d_current_index;
        // Rewind current_index if needed
        while (current_index >= 1 && d_times[current_index] > time) {
            --current_index;
        }
        // Advance current_index so that the next time is greater than the
        // current.
        while (current_index + 1 < d_times.size() && d_times[current_index + 1] <= time) {
            ++current_index;
        }
        if ((time < d_times[current_index]) || (current_index + 1 == d_times.size())) {
            // We are before the beginning or past the end of the file, so we
            // maintain a constant delay.
            return d_delays_samples[current_index];
        }
        // Linearly interpolate delay
        double alpha = (time - d_times[current_index]) /
                       (d_times[current_index + 1] - d_times[current_index]);
        return (1.0 - alpha) * d_delays_samples[current_index] +
               alpha * d_delays_samples[current_index + 1];
    }

public:
    time_dependent_delay_impl(const std::string& filename,
                              double samp_rate,
                              double t0,
                              const std::vector<float>& taps,
                              int num_filters);
    ~time_dependent_delay_impl() override;

    void set_time(double) override;

    double time() override
    {
        gr::thread::scoped_lock guard(d_setlock);
        return d_current_time;
    }

    double delay() override
    {
        gr::thread::scoped_lock guard(d_setlock);
        return d_current_delay / d_samp_rate;
    }

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items) override;
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_TIME_DEPENDENT_DELAY_IMPL_H */
