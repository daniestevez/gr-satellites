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
#include "ao40_deinterleaver_impl.h"

#define ROWS 80
#define COLS 65
#define OUT_SIZE 5132

namespace gr {
  namespace satellites {

    ao40_deinterleaver::sptr
    ao40_deinterleaver::make()
    {
      return gnuradio::get_initial_sptr
        (new ao40_deinterleaver_impl());
    }

    /*
     * The private constructor
     */
    ao40_deinterleaver_impl::ao40_deinterleaver_impl()
      : gr::block("ao40_deinterleaver",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(0, 0, 0))
    {
      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"),
		      boost::bind(&ao40_deinterleaver_impl::msg_handler, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    ao40_deinterleaver_impl::~ao40_deinterleaver_impl()
    {
    }

    void
    ao40_deinterleaver_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    }

    int
    ao40_deinterleaver_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        return 0;
    }


    void
    ao40_deinterleaver_impl::msg_handler (pmt::pmt_t pmt_msg) {
      pmt::pmt_t msg = pmt::cdr(pmt_msg);
      size_t offset(0);
      const uint8_t *data = (const uint8_t *) pmt::uniform_vector_elements(msg, offset);
      float out[OUT_SIZE];

      for (int i = 0; i < OUT_SIZE; i++) {
	out[i] = -1.0 + 2.0 * data[ROWS*(i % COLS) + i/COLS + 1];
      }

      message_port_pub(pmt::mp("out"),
		       pmt::cons(pmt::PMT_NIL,
				 pmt::init_f32vector(OUT_SIZE, out)));
      
    }
    

  } /* namespace satellites */
} /* namespace gr */

