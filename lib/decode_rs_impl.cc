/* -*- c++ -*- */
/*
 * Copyright 2016 Daniel Estevez <daniel@destevez.net>
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
#include "decode_rs_impl.h"

#include <cstdio>

extern "C" {
#include <gnuradio/fec/rs.h>
}

#include "rs.h"

// This should be included in <gnuradio/fec/rs.h>
extern int decode_rs_ccsds(unsigned char *data,int *eras_pos,int no_eras);

namespace gr {
  namespace satellites {

    decode_rs::sptr
    decode_rs::make(bool verbose, int basis)
    {
      return gnuradio::get_initial_sptr
        (new decode_rs_impl(verbose, basis));
    }

    /*
     * The private constructor
     */
    decode_rs_impl::decode_rs_impl(bool verbose, int basis)
      : gr::block("decode_rs",
		  gr::io_signature::make(0, 0, 0),
		  gr::io_signature::make(0, 0, 0))
    {
      d_verbose = verbose;
      d_basis = basis;

      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"),
		      boost::bind(&decode_rs_impl::msg_handler, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    decode_rs_impl::~decode_rs_impl()
    {
    }

    void
    decode_rs_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    }

    int
    decode_rs_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      return 0;
    }

    void
    decode_rs_impl::msg_handler (pmt::pmt_t pmt_msg) {
      pmt::pmt_t msg = pmt::cdr(pmt_msg);
      uint8_t data[MAX_FRAME_LEN];
      int rs_res;
      int frame_len = pmt::length(msg);
      size_t offset(0);

      if (frame_len <= 32 || frame_len > MAX_FRAME_LEN) {
      	if (d_verbose) {
	  std::printf("Reed-Solomon decoder: invalid frame length %d\n", frame_len);
	  return;
	}
      }

      // Add zero padding to the beginning of the message
      // This is discarded after RS decoding
      int padding = MAX_FRAME_LEN - frame_len;
      std::memset(data, 0, padding);
      std::memcpy(data + padding, pmt::uniform_vector_elements(msg, offset), frame_len);

      if (d_basis == BASIS_CONVENTIONAL) {
	rs_res = decode_rs_8(data, NULL, 0);
      }
      else {
	rs_res = decode_rs_ccsds(data, NULL, 0);
      }

      // Send via GNUradio message if RS ok
      if (rs_res >= 0) {
	frame_len -= 32;

	if (d_verbose) {
	  std::printf("Reed-Solomon decode OK. Bytes corrected: %d.\n", rs_res);
	}

	// Send by GNUradio message
	message_port_pub(pmt::mp("out"),
			 pmt::cons(pmt::PMT_NIL,
				   pmt::init_u8vector(frame_len, data + padding)));
      }
      else if (d_verbose) {
	std::printf("Reed-Solomon decode failed.\n");
      }
    }
    
  } /* namespace satellites */
} /* namespace gr */

