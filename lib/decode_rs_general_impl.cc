/* -*- c++ -*- */
/* 
 * Copyright 2018 Daniel Estevez <daniel@destevez.net>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "decode_rs_general_impl.h"

#include <cstdio>

#include <string.h>

#include "rs.h"

extern "C" {
#include <fec.h>
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
      : gr::block("decode_rs",
		  gr::io_signature::make(0, 0, 0),
		  gr::io_signature::make(0, 0, 0))
    {
      d_verbose = verbose;

      d_nroots = nroots;
      d_rs = init_rs_char(8, gfpoly, fcr, prim, nroots, 0); // TODO handle error

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
      pmt::pmt_t msg = pmt::cdr(pmt_msg);
      uint8_t data[MAX_FRAME_LEN];
      int rs_res;
      int frame_len = pmt::length(msg);
      size_t offset(0);

      assert(frame_len <= MAX_FRAME_LEN);

      memset(data, 0, sizeof(data));
      memcpy(data, pmt::uniform_vector_elements(msg, offset), frame_len);

      rs_res = decode_rs_char(d_rs, data, NULL, 0);

      // Send via GNUradio message if RS ok
      if (rs_res >= 0) {
	frame_len -= d_nroots;

	if (d_verbose) {
	  std::printf("Reed-Solomon decode OK. Bytes corrected: %d.\n", rs_res);
	}

	// Send by GNUradio message
	message_port_pub(pmt::mp("out"),
			 pmt::cons(pmt::PMT_NIL,
				   pmt::init_u8vector(frame_len, data)));
      }
      else if (d_verbose) {
	std::printf("Reed-Solomon decode failed.\n");
      }
    }
    
  } /* namespace satellites */
} /* namespace gr */

