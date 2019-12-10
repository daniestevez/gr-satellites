/* -*- c++ -*- */
/* 
 * Copyright 2019 Daniel Estevez <daniel@destevez.net>.
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
#include "decode_ra_code_impl.h"

extern "C" {
#include "radecoder/ra_decoder.h"
}

namespace gr {
  namespace satellites {

    decode_ra_code::sptr
    decode_ra_code::make(int size)
    {
      return gnuradio::get_initial_sptr
        (new decode_ra_code_impl(size));
    }

    /*
     * The private constructor
     */
    decode_ra_code_impl::decode_ra_code_impl(int size)
      : gr::block("decode_ra_code",
		  gr::io_signature::make(0, 0, 0),
		  gr::io_signature::make(0, 0, 0))
    {
      d_size = size;

      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"),
		      boost::bind(&decode_ra_code_impl::msg_handler, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    decode_ra_code_impl::~decode_ra_code_impl()
    {
    }

    void
    decode_ra_code_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    }

    int
    decode_ra_code_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      return 0;
    }

    void
    decode_ra_code_impl::msg_handler (pmt::pmt_t pmt_msg) {
      pmt::pmt_t msg = pmt::cdr(pmt_msg);
      uint8_t *ra_out = new uint8_t [d_size];
      size_t offset(0);

      memset(ra_out, 0, d_size);
      ra_decode((const uint8_t*) pmt::uniform_vector_elements(msg, offset), ra_out, d_size);

      message_port_pub(pmt::mp("out"),
		       pmt::cons(pmt::PMT_NIL,
				   pmt::init_u8vector(d_size, ra_out)));
    }
    
  } /* namespace satellites */
} /* namespace gr */

