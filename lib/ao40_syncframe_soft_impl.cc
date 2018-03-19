/* -*- c++ -*- */
/*
 * Copyright 2018 Daniel Estevez <daniel@destevez.net>.
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
#include "ao40_syncframe_soft_impl.h"

#define STEP 80

namespace gr {
  namespace satellites {

    ao40_syncframe_soft::sptr
    ao40_syncframe_soft::make(int threshold)
    {
      return gnuradio::get_initial_sptr
        (new ao40_syncframe_soft_impl(threshold));
    }

    const uint8_t ao40_syncframe_soft_impl::d_syncword[] =
      {1,1,1,1,1,1,1,0,0,0,0,1,1,1,0,1,1,1,1,0,0,1,0,1,1,0,0,1,0,0,
      1,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,0,0,0,1,0,1,1,1,0,1,0,1,1,0,1,1,0,0,0};

    /*
     * The private constructor
     */
    ao40_syncframe_soft_impl::ao40_syncframe_soft_impl(int threshold)
      : gr::sync_block("ao40_syncframe_soft",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(0, 0, 0))
    {
      d_threshold = threshold;
      set_history(SYNCLEN * STEP);

      message_port_register_out(pmt::mp("out"));
    }

    /*
     * Our virtual destructor.
     */
    ao40_syncframe_soft_impl::~ao40_syncframe_soft_impl()
    {
    }

    int
    ao40_syncframe_soft_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      int match;

      const float *in = (const float *) input_items[0];

      for (int i = 0; i < noutput_items; i++) {
	match = 0;
	for (int j = 0; j < SYNCLEN; j++) {
	  match += (in[i + j * STEP] >= 0.0) ^ d_syncword[j];
	}
	if (match >= SYNCLEN - d_threshold) {
	  // sync found
	  message_port_pub(pmt::mp("out"),
			   pmt::cons(pmt::PMT_NIL,
				     pmt::init_f32vector(SYNCLEN * STEP, in + i)));
	}
      }

      return noutput_items;
    }

  } /* namespace satellites */
} /* namespace gr */

