/* -*- c++ -*- */
/*
 * Copyright 2019 Daniel Estevez <daniel@destevez.net>
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
#include "decode_rs_interleaved_impl.h"

#include <cstdio>

extern "C" {
#include "libfec/fec.h"
}

#include "rs.h"

namespace gr {
  namespace satellites {

    decode_rs_interleaved::sptr
    decode_rs_interleaved::make(bool verbose, int basis, int codewords)
    {
      return gnuradio::get_initial_sptr
        (new decode_rs_interleaved_impl(verbose, basis, codewords));
    }

    /*
     * The private constructor
     */
    decode_rs_interleaved_impl::decode_rs_interleaved_impl(bool verbose, int basis, int codewords)
      : gr::block("decode_rs",
		  gr::io_signature::make(0, 0, 0),
		  gr::io_signature::make(0, 0, 0))
    {
      d_verbose = verbose;
      d_basis = basis;
      d_codewords = codewords;

      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"),
		      boost::bind(&decode_rs_interleaved_impl::msg_handler, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    decode_rs_interleaved_impl::~decode_rs_interleaved_impl()
    {
    }

    void
    decode_rs_interleaved_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    }

    int
    decode_rs_interleaved_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      return 0;
    }

    void
    decode_rs_interleaved_impl::msg_handler (pmt::pmt_t pmt_msg) {
      pmt::pmt_t msg = pmt::cdr(pmt_msg);
      uint8_t* codeword = new uint8_t[MAX_FRAME_LEN];
      uint8_t* data_in = new uint8_t[MAX_FRAME_LEN * d_codewords];
      uint8_t* data_out = new uint8_t[(MAX_FRAME_LEN - 32) * d_codewords];
      int rs_res, total_errors = 0;
      int frame_len = pmt::length(msg);
      size_t offset(0);

      if (frame_len != MAX_FRAME_LEN * d_codewords) {
      	if (d_verbose) {
	  std::printf("Reed-Solomon decoder: invalid frame length %d\n", frame_len);
	  return;
	}
      }

      memcpy(data_in, pmt::uniform_vector_elements(msg, offset), frame_len);
      
      for (int j = 0; j < d_codewords; j++) {
	for (int k = 0; k < MAX_FRAME_LEN; k++) {
	  codeword[k] = data_in[j + d_codewords * k];
	}
	
	if (d_basis == BASIS_CONVENTIONAL) {
	  rs_res = decode_rs_8(codeword, NULL, 0, 0);
	}
	else {
	  rs_res = decode_rs_ccsds(codeword, NULL, 0, 0);
	}

	if (rs_res < 0) {
	  if (d_verbose) {
	    std::printf("Reed-Solomon decode failed.\n");
	  }
	  return;
	}

	total_errors += rs_res;

	for (int k = 0; k < MAX_FRAME_LEN - 32; k++) {
	  data_out[j + d_codewords * k] = codeword[k];
	}
      }

      if (d_verbose) {
	std::printf("Reed-Solomon decode OK. Bytes corrected: %d.\n", total_errors);
      }

      // Send by GNUradio message
      message_port_pub(pmt::mp("out"),
		       pmt::cons(pmt::PMT_NIL,
				 pmt::init_u8vector(frame_len - 32 * d_codewords, data_out)));
    }
    
  } /* namespace satellites */
} /* namespace gr */

