/* -*- c++ -*- */
/*
 * Copyright 2022 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "phase_unwrap_impl.h"
#include <gnuradio/io_signature.h>
#include <cstring>

// Output is (int64_t, float)
#define OUTPUT_SIZE (sizeof(int64_t) + sizeof(float))

namespace gr {
namespace satellites {

phase_unwrap::sptr phase_unwrap::make()
{
    return gnuradio::make_block_sptr<phase_unwrap_impl>();
}


phase_unwrap_impl::phase_unwrap_impl()
    : gr::sync_block("phase_unwrap",
                     gr::io_signature::make(1, 1, sizeof(float)),
                     gr::io_signature::make(1, 1, OUTPUT_SIZE)),
      d_integer_cycles(0.0),
      d_last_phase(GR_M_PI)
{
}

phase_unwrap_impl::~phase_unwrap_impl() {}

int phase_unwrap_impl::work(int noutput_items,
                            gr_vector_const_void_star& input_items,
                            gr_vector_void_star& output_items)
{
    auto in = static_cast<const float*>(input_items[0]);
    auto out = static_cast<uint8_t*>(output_items[0]);

    for (int j = 0; j < noutput_items; ++j) {
        float phase = phase_wrap(in[j]);
        if ((d_last_phase < GR_M_PI / 2.0) && (phase > 3.0 * GR_M_PI / 2.0)) {
            --d_integer_cycles;
        } else if ((d_last_phase > 3.0 * GR_M_PI / 2.0) && (phase < GR_M_PI / 2.0)) {
            ++d_integer_cycles;
        }
        d_last_phase = phase;
        std::memcpy(&out[j * OUTPUT_SIZE], &d_integer_cycles, sizeof(int64_t));
        std::memcpy(&out[j * OUTPUT_SIZE + sizeof(int64_t)], &phase, sizeof(float));
    }

    return noutput_items;
}

} /* namespace satellites */
} /* namespace gr */
