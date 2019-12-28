/* -*- c++ -*- */
/*
 * Copyright 2019 Daniel Estevez <daniel@destevez.net>.
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
#include "matrix_deinterleaver_soft_impl.h"

namespace gr {
  namespace satellites {

    matrix_deinterleaver_soft::sptr
    matrix_deinterleaver_soft::make(int rows, int cols, int output_size, int output_skip)
    {
      return gnuradio::get_initial_sptr
        (new matrix_deinterleaver_soft_impl(rows, cols, output_size, output_skip));
    }

    /*
     * The private constructor
     */
    matrix_deinterleaver_soft_impl::matrix_deinterleaver_soft_impl(int rows, int cols, int output_size, int output_skip)
      : gr::block("matrix_deinterleaver_soft",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(0, 0, 0))
    {
      d_rows = rows;
      d_cols = cols;
      d_output_size = output_size;
      d_output_skip = output_skip;
      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"),
		      boost::bind(&matrix_deinterleaver_soft_impl::msg_handler, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    matrix_deinterleaver_soft_impl::~matrix_deinterleaver_soft_impl()
    {
    }

    void
    matrix_deinterleaver_soft_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    }

    int
    matrix_deinterleaver_soft_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        return 0;
    }


    void
    matrix_deinterleaver_soft_impl::msg_handler (pmt::pmt_t pmt_msg) {
      pmt::pmt_t msg = pmt::cdr(pmt_msg);
      size_t offset(0);
      const float *data = (const float *) pmt::uniform_vector_elements(msg, offset);
      float *out = new float [d_rows * d_cols];

      // Full matrix deinterleave, ignoring output cropping
      for (int i = 0; i < d_rows * d_cols; i++) {
	out[i] = data[d_rows*(i % d_cols) + i/d_cols];
      }

      // Output cropping
      message_port_pub(pmt::mp("out"),
		       pmt::cons(pmt::PMT_NIL,
				 pmt::init_f32vector(d_output_size, out + d_output_skip)));
      
    }
    

  } /* namespace satellites */
} /* namespace gr */

