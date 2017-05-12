/* -*- c++ -*- */
/*
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "ao40_rs_decoder_impl.h"

#include <cstdio>

extern "C" {
#include <fec.h>
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
              gr::io_signature::make(0, 0, 0))
    {
      d_verbose = verbose;

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
      pmt::pmt_t msg = pmt::cdr(pmt_msg);
      size_t offset(0);
      const uint8_t *data = (const uint8_t *) pmt::uniform_vector_elements(msg, offset);
      uint8_t scratch[N];
      uint8_t message[2*K];
      int i;
      int rs_res[2];

      if (pmt::length(msg) != 2*N) return;

      for (int dec = 0; dec < 2; dec++) {
	for (i = 0; i < N; i++) {
	  scratch[i] = data[2*i + dec] ^ 0xff; // data needs to be inverted for some reason
	}
	rs_res[dec] = decode_rs_8(scratch, NULL, 0, 255 - N);
	if (rs_res[0] == -1) {
	  if (d_verbose) {
	    printf("Reed-Solomon decode failed (%dst decoder).\n", dec + 1);
	  }
	  return;
	}
	else {
	  for (i = 0; i < K; i++) {
	    message[2*i + dec] = scratch[i];
	  }
	}
      }

      if (d_verbose) {
	printf("Reed-Solomon decode OK. Bytes corrected %d, %d.\n", rs_res[0], rs_res[1]);
      }
      
      message_port_pub(pmt::mp("out"),
		       pmt::cons(pmt::PMT_NIL,
				 pmt::init_u8vector(2*K, message)));
      
    }

  } /* namespace satellites */
} /* namespace gr */

