/* -*- c++ -*- */
/* 
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>.
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

#include <gnuradio/logger.h>

#include <gnuradio/io_signature.h>
#include "rscode_decoder_impl.h"

extern "C" {
#include "rscode/ecc.h"
}

namespace gr {
  namespace satellites {

    rscode_decoder::sptr
    rscode_decoder::make(int npar)
    {
      return gnuradio::get_initial_sptr
        (new rscode_decoder_impl(npar));
    }

    /*
     * The private constructor
     */
    rscode_decoder_impl::rscode_decoder_impl(int npar)
      : gr::block("rscode_decoder",
              gr::io_signature::make(0, 0, 0),
	      gr::io_signature::make(0, 0, 0))
    {
      // Initialize Galois tables and polynomial for Reed-Solomon
      d_npar = npar;
      initialize_ecc(d_npar);
      
      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"),
		      boost::bind(&rscode_decoder_impl::msg_handler, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    rscode_decoder_impl::~rscode_decoder_impl()
    {
    }

    void
    rscode_decoder_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    }

    int
    rscode_decoder_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      return 0;
    }

    void
    rscode_decoder_impl::msg_handler (pmt::pmt_t pmt_msg) {
      pmt::pmt_t msg = pmt::cdr(pmt_msg);
      uint8_t data[RS_LEN];
      int length;
      size_t offset(0);

      length = std::min(pmt::length(msg), sizeof(data));
      memcpy(data, pmt::uniform_vector_elements(msg, offset), length);

      // Reed-Solomon decoding
      decode_data(data, length);
      if (check_syndrome() != 0) {
	if (correct_errors_erasures(data, length, 0, NULL) != 1) {
	  GR_LOG_INFO(d_logger, "Reed-Solomon decoding failed");
	  return;
	}
        else {
	  GR_LOG_INFO(d_logger, "Reed-Solomon corrected errors");
	}
      }
      else {
	GR_LOG_INFO(d_logger, "Reed-Solomon found no errors");
      }
      
      // Send by GNUradio message
      message_port_pub(pmt::mp("out"),
		       pmt::cons(pmt::PMT_NIL,
				 pmt::init_u8vector(length-d_npar, data)));
    }
  } /* namespace satellites */
} /* namespace gr */

