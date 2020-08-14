/* -*- c++ -*- */
/*
 * Copyright 2018 Daniel Estevez <daniel@destevez.net>
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
#include "decode_rs_general_impl.h"

#include <cstdio>
#include <new>

#include <string.h>

#include "rs.h"

extern "C" {
#include "libfec/fec.h"
}

namespace gr {
  namespace satellites {

    decode_rs_general::sptr
    decode_rs_general::make(int gfpoly, int fcr, int prim, int nroots, bool verbose)
    {
      return gnuradio::get_initial_sptr
        (new decode_rs_general_impl(gfpoly, fcr, prim, nroots, verbose));
    }

    /*
     * The private constructor
     */
    decode_rs_general_impl::decode_rs_general_impl(int gfpoly, int fcr, int prim, int nroots, bool verbose)
      : gr::block("decode_rs_general",
		  gr::io_signature::make(0, 0, 0),
		  gr::io_signature::make(0, 0, 0)),
	d_verbose(verbose),
	d_nroots(nroots)
    {
      d_rs = init_rs_char(8, gfpoly, fcr, prim, nroots, 0);
      if (!d_rs) throw std::bad_alloc();

      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"),
		      boost::bind(&decode_rs_general_impl::msg_handler, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    decode_rs_general_impl::~decode_rs_general_impl()
    {
      free_rs_char(d_rs);
    }

    void
    decode_rs_general_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    }

    int
    decode_rs_general_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      return 0;
    }

    void
    decode_rs_general_impl::msg_handler (pmt::pmt_t pmt_msg) {
      size_t length(0);
      auto msg = pmt::u8vector_elements(pmt::cdr(pmt_msg), length);

      if (length <= d_nroots || length > d_data.size()) {
      	if (d_verbose) {
	  std::printf("Reed-Solomon decoder: invalid frame length %ld\n", (long) length);
	}
	return;
      }

      d_data.fill(0);
      memcpy(d_data.data(), msg, length);

      auto rs_res = decode_rs_char(d_rs, d_data.data(), NULL, 0);

      // Send via GNUradio message if RS ok
      if (rs_res >= 0) {
        length -= d_nroots;

	if (d_verbose) {
	  std::printf("Reed-Solomon decode OK. Bytes corrected: %d.\n", rs_res);
	}

	// Send by GNUradio message
	message_port_pub(pmt::mp("out"),
			 pmt::cons(pmt::PMT_NIL,
				   pmt::init_u8vector(length, d_data.data())));
      }
      else if (d_verbose) {
	std::printf("Reed-Solomon decode failed.\n");
      }
    }
    
  } /* namespace satellites */
} /* namespace gr */

