/* -*- c++ -*- */
/*
 * Copyright 2022 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_PHASE_UNWRAP_IMPL_H
#define INCLUDED_SATELLITES_PHASE_UNWRAP_IMPL_H

#include <gnuradio/math.h>
#include <satellites/phase_unwrap.h>
#include <cstdint>

namespace gr {
namespace satellites {

class phase_unwrap_impl : public phase_unwrap
{
private:
    int64_t d_integer_cycles;
    float d_last_phase;

    // Implementation taken from gr::block::control_loop but modified to yield
    // values in [0, 2pi).
    inline float phase_wrap(float phase) const
    {
        while (phase > (2 * GR_M_PI))
            phase -= 2 * GR_M_PI;
        while (phase < 0)
            phase += 2 * GR_M_PI;
        return phase;
    }

public:
    phase_unwrap_impl();
    ~phase_unwrap_impl();

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_PHASE_UNWRAP_IMPL_H */
