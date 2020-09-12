/* -*- c++ -*- */
/*
 * Copyright 2018,2020 Daniel Estevez <daniel@destevez.net>
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
#include "encode_rs_impl.h"

#include <cstdio>

extern "C" {
#include "libfec/fec.h"
}

#include "rs.h"

namespace gr {
  namespace satellites {

    encode_rs::sptr
    encode_rs::make(int basis)
    {
      return gnuradio::get_initial_sptr
        (new encode_rs_impl(basis));
    }

    /*
     * The private constructor
     */
    encode_rs_impl::encode_rs_impl(int basis)
      : gr::block("encode_rs",
		  gr::io_signature::make(0, 0, 0),
		  gr::io_signature::make(0, 0, 0)),
	d_basis(basis)
    {
      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"),
		      boost::bind(&encode_rs_impl::msg_handler, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    encode_rs_impl::~encode_rs_impl()
    {
    }

    void
    encode_rs_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    }

    int
    encode_rs_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      return 0;
    }

    void
    encode_rs_impl::msg_handler (pmt::pmt_t pmt_msg) {
      size_t length(0);
      auto msg = pmt::u8vector_elements(pmt::cdr(pmt_msg), length);

      if (length > MAX_FRAME_LEN - PARITY_BYTES) return;

      memcpy(d_data.data(), msg, length);

      if (d_basis == BASIS_CONVENTIONAL) {
	encode_rs_8(d_data.data(), &d_data[length],
		    MAX_FRAME_LEN - length - PARITY_BYTES);
      }
      else {
	encode_rs_ccsds(d_data.data(), &d_data[length],
			MAX_FRAME_LEN - length - PARITY_BYTES);
      }

      // Send by GNUradio message
      message_port_pub(pmt::mp("out"),
		       pmt::cons(pmt::PMT_NIL,
				 pmt::init_u8vector(length + PARITY_BYTES, d_data.data())));
    }
  } /* namespace satellites */
} /* namespace gr */

