/* -*- c++ -*- */
/*
 * Copyright 2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "nrzi_encode_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
namespace satellites {

nrzi_encode::sptr nrzi_encode::make()
{
    return gnuradio::make_block_sptr<nrzi_encode_impl>();
}

/*
 * The private constructor
 */
nrzi_encode_impl::nrzi_encode_impl()
    : gr::sync_block("nrzi_encode",
                     gr::io_signature::make(1, 1, sizeof(uint8_t)),
                     gr::io_signature::make(1, 1, sizeof(uint8_t))),
      d_last(0)
{
}

/*
 * Our virtual destructor.
 */
nrzi_encode_impl::~nrzi_encode_impl() {}

int nrzi_encode_impl::work(int noutput_items,
                           gr_vector_const_void_star& input_items,
                           gr_vector_void_star& output_items)
{
    const uint8_t* in = (const uint8_t*)input_items[0];
    uint8_t* out = (uint8_t*)output_items[0];

    for (int i = 0; i < noutput_items; ++i) {
        out[i] = d_last = ~(in[i] ^ d_last) & 1;
    }

    return noutput_items;
}


} /* namespace satellites */
} /* namespace gr */
