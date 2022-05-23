/* -*- c++ -*- */
/*
 * Copyright 2022 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_COSTAS_LOOP_8APSK_CC_IMPL_H
#define INCLUDED_SATELLITES_COSTAS_LOOP_8APSK_CC_IMPL_H

#include <gnuradio/math.h>
#include <satellites/costas_loop_8apsk_cc.h>

namespace gr {
namespace satellites {

class costas_loop_8apsk_cc_impl : public costas_loop_8apsk_cc
{
private:
    float d_error;

    float phase_detector(gr_complex sample) const
    {
        if (sample.real() * sample.real() + sample.imag() * sample.imag() < 0.25) {
            return 0;
        }
        float phase = gr::fast_atan2f(sample.imag(), sample.real());
        return fmodf(phase + GR_M_PI, 2.0 * GR_M_PI / 7.0) - GR_M_PI / 7.0;
    }

public:
    costas_loop_8apsk_cc_impl(float loop_bw);
    ~costas_loop_8apsk_cc_impl();

    float error() const override { return d_error; };

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_COSTAS_LOOP_8APSK_CC_IMPL_H */
