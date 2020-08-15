/* -*- c++ -*- */
/*
 * Copyright 2017,2020 Daniel Estevez <daniel@destevez.net>
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
#include "ao40_rs_decoder_impl.h"

#include <cstdio>

extern "C" {
#include "libfec/fec.h"
}

#define N (128 + 32)
#define K 128

namespace gr {
  namespace satellites {

    ao40_rs_decoder::sptr
    ao40_rs_decoder::make(bool verbose)
    {
      return gnuradio::get_initial_sptr
        (new ao40_rs_decoder_impl(verbose));
    }

    /*
     * The private constructor
     */
    ao40_rs_decoder_impl::ao40_rs_decoder_impl(bool verbose)
      : gr::block("ao40_rs_decoder",
	      gr::io_signature::make(0, 0, 0),
	      gr::io_signature::make(0, 0, 0)),
	d_verbose(verbose)
    {
      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"),
		      boost::bind(&ao40_rs_decoder_impl::msg_handler, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    ao40_rs_decoder_impl::~ao40_rs_decoder_impl()
    {
    }

    void
    ao40_rs_decoder_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
    }

    int
    ao40_rs_decoder_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      return 0;
    }

    void
    ao40_rs_decoder_impl::msg_handler (pmt::pmt_t pmt_msg) {
      size_t length(0);
      auto data = pmt::u8vector_elements(pmt::cdr(pmt_msg), length);
      int rs_res[2];

      if (length != 2 * d_n) return;

      for (size_t dec = 0; dec < 2; ++dec) {
	for (size_t i = 0; i < d_scratch.size(); ++i) {
	  d_scratch[i] = data[2*i + dec];
	}
	rs_res[dec] = decode_rs_8(d_scratch.data(), NULL, 0, 255 - d_n);
	if (rs_res[dec] == -1) {
	  if (d_verbose) {
	    std::printf("Reed-Solomon decode failed (%dst decoder).\n", int(dec + 1));
	  }
	  return;
	}
	else {
	  for (size_t i = 0; i < d_k; ++i) {
	    d_message[2*i + dec] = d_scratch[i];
	  }
	}
      }

      if (d_verbose) {
	printf("Reed-Solomon decode OK. Bytes corrected %d, %d.\n", rs_res[0], rs_res[1]);
      }
      
      message_port_pub(pmt::mp("out"),
		       pmt::cons(pmt::PMT_NIL,
				 pmt::init_u8vector(d_message.size(), d_message.data())));
      
    }

  } /* namespace satellites */
} /* namespace gr */

