/* -*- c++ -*- */
/*
 * Copyright 2022-2023,2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_DOPPLER_CORRECTION_IMPL_H
#define INCLUDED_SATELLITES_DOPPLER_CORRECTION_IMPL_H

#include <gnuradio/math.h>
#include <satellites/doppler_correction.h>
#include <cstdint>
#include <vector>

namespace gr {
namespace satellites {

class doppler_correction_impl : public doppler_correction
{
private:
    double d_phase;
    double d_samp_rate;
    size_t d_current_index;
    double d_t0;
    uint64_t d_sample_t0;
    std::vector<double> times;
    std::vector<double> freqs_rad_per_sample;
    std::vector<tag_t> d_tags;

    // Used by UHD
    const pmt::pmt_t d_rx_time_key;

    // Used by gr-difi
    const pmt::pmt_t d_pck_n_key;
    const pmt::pmt_t d_full_key;
    const pmt::pmt_t d_frac_key;

    // timesync tag
    const bool d_timesync_enabled;
    const pmt::pmt_t d_timesync_key;

    double d_current_time;
    double d_current_freq;

    // Implementation taken from gr::block::control_loop
    void phase_wrap()
    {
        while (d_phase > (2 * GR_M_PI))
            d_phase -= 2 * GR_M_PI;
        while (d_phase < (-2 * GR_M_PI))
            d_phase += 2 * GR_M_PI;
    }

    // Called after a time update. Makes the current index go backwards if
    // needed because of a time update "to the past".
    void adjust_current_index()
    {
        while ((d_current_index > 0) && (times[d_current_index] > d_t0)) {
            --d_current_index;
        }
    }

    void read_doppler_file(const std::string& filename);

public:
    doppler_correction_impl(const std::string& filename,
                            double samp_rate,
                            double t0,
                            const std::string& timesync_tag);
    ~doppler_correction_impl() override;

    void set_time(double) override;

    double time() override
    {
        gr::thread::scoped_lock guard(d_setlock);
        return d_current_time;
    }

    double frequency() override
    {
        gr::thread::scoped_lock guard(d_setlock);
        return d_current_freq * d_samp_rate / (2.0 * GR_M_PI);
    }

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items) override;
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_DOPPLER_CORRECTION_IMPL_H */
