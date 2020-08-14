/* -*- c++ -*- */
/* 
 * Copyright 2016 Daniel Estevez <daniel@destevez.net>.
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

#include <algorithm>
#include <utility>

#include <cstdio>
#include <cstring>

#include <gnuradio/io_signature.h>
#include "ax100_decode_impl.h"

extern "C" {
#include "libfec/fec.h"
}

namespace gr {
  namespace satellites {

    ax100_decode::sptr
    ax100_decode::make(bool verbose)
    {
      return gnuradio::get_initial_sptr
        (new ax100_decode_impl(verbose));
    }

    /*
     * The private constructor
     */
    ax100_decode_impl::ax100_decode_impl(bool verbose)
      : gr::block("ax100_decode",
	      gr::io_signature::make(0, 0, 0),
	      gr::io_signature::make(0, 0, 0)),
	d_verbose(verbose)
    {
      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"),
		      boost::bind(&ax100_decode_impl::msg_handler, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    ax100_decode_impl::~ax100_decode_impl()
    {
    }

    void
    ax100_decode_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    }

    int
    ax100_decode_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        return 0;
    }

    void
    ax100_decode_impl::msg_handler (pmt::pmt_t pmt_msg) {
      size_t length(0);
      auto msg = pmt::u8vector_elements(pmt::cdr(pmt_msg), length);

      length = std::min(length, d_data.size());
      std::memcpy(d_data.data(), msg, length);

      auto rs_res = decode_rs_8(&d_data[1], NULL, 0, 255 - d_data[0] + 1);

      // Send via GNUradio message if RS ok
      if (rs_res >= 0) {
	// Swap CSP header
	std::swap(d_data[1], d_data[4]);
	std::swap(d_data[2], d_data[3]);

	// 32 RS parity symbols, 1 includes the length byte
	auto frame_len = d_data[0] - 32 - 1;
	if (frame_len < 0) {
	  return;
	}

	if (d_verbose) {
	  std::printf("RS decode OK. Length: %d. Bytes corrected: %d.\n", frame_len, rs_res);
	}

	// Send by GNUradio message
	message_port_pub(pmt::mp("out"),
			 pmt::cons(pmt::PMT_NIL,
				   pmt::init_u8vector(frame_len, &d_data[1])));
      }
      else if (d_verbose) {
	std::printf("RS decode failed.\n");
      }
      
      
    }

  } /* namespace satellites */
} /* namespace gr */

