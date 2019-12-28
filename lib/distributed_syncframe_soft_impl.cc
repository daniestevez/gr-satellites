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
#include "distributed_syncframe_soft_impl.h"

namespace gr {
  namespace satellites {

    distributed_syncframe_soft::sptr
    distributed_syncframe_soft::make(int threshold, const std::string& syncword, int step)
    {
      return gnuradio::get_initial_sptr
        (new distributed_syncframe_soft_impl(threshold, syncword, step));
    }

    /*
     * The private constructor
     */
    distributed_syncframe_soft_impl::distributed_syncframe_soft_impl(int threshold, const std::string& syncword, int step)
      : gr::sync_block("distributed_syncframe_soft",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(0, 0, 0))
    {
      d_threshold = threshold;
      d_step = step;
      d_synclen = syncword.length();

      d_syncword = new uint8_t [d_synclen];
      
      for (int i = 0; i < d_synclen; i++) {
	d_syncword[i] = syncword[i] & 1; // look at LSB only, as in correlate_access_code_bb_impl.cc
      }
            
      set_history(d_synclen * d_step);

      message_port_register_out(pmt::mp("out"));
    }

    /*
     * Our virtual destructor.
     */
    distributed_syncframe_soft_impl::~distributed_syncframe_soft_impl()
    {
    }

    int
    distributed_syncframe_soft_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      int match;

      const float *in = (const float *) input_items[0];

      for (int i = 0; i < noutput_items; i++) {
	match = 0;
	for (int j = 0; j < d_synclen; j++) {
	  match += (in[i + j * d_step] < 0.0) ^ d_syncword[j];
	}
	if (match >= d_synclen - d_threshold) {
	  // sync found
	  message_port_pub(pmt::mp("out"),
			   pmt::cons(pmt::PMT_NIL,
				     pmt::init_f32vector(d_synclen * d_step, in + i)));
	}
      }

      return noutput_items;
    }

  } /* namespace satellites */
} /* namespace gr */

