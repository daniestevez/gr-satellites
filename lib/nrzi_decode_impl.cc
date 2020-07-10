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

#include <gnuradio/io_signature.h>
#include "nrzi_decode_impl.h"

namespace gr {
  namespace satellites {

    nrzi_decode::sptr
    nrzi_decode::make()
    {
      return gnuradio::get_initial_sptr
        (new nrzi_decode_impl());
    }

    /*
     * The private constructor
     */
    nrzi_decode_impl::nrzi_decode_impl()
      : gr::sync_block("nrzi_decode",
		       gr::io_signature::make(1, 1, sizeof(uint8_t)),
		       gr::io_signature::make(1, 1, sizeof(uint8_t))),
	d_last(0)
    {
    }

    /*
     * Our virtual destructor.
     */
    nrzi_decode_impl::~nrzi_decode_impl()
    {
    }

    int
    nrzi_decode_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const uint8_t *in = (const uint8_t *) input_items[0];
      uint8_t *out = (uint8_t *) output_items[0];

      for (int i = 0; i < noutput_items; ++i) {
	out[i] = ~(in[i] ^ d_last) & 1;
	d_last = in[i];
      }

      return noutput_items;
    }

    
  } /* namespace satellites */
} /* namespace gr */

