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
#include "descrambler308_impl.h"

namespace gr {
  namespace satellites {

    descrambler308::sptr
    descrambler308::make()
    {
      return gnuradio::get_initial_sptr
        (new descrambler308_impl());
    }

    /*
     * The private constructor
     */
    descrambler308_impl::descrambler308_impl()
      : gr::sync_block("descrambler308",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
      d_counter = 0;
      d_shift_register = 0;
    }

    /*
     * Our virtual destructor.
     */
    descrambler308_impl::~descrambler308_impl()
    {
    }

    int
    descrambler308_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];

      for (int i = 0; i < noutput_items; i++) {
	out[i] = d_scramble_bit(in[i]);
      }

      return noutput_items;
    }

    unsigned char
    descrambler308_impl::d_scramble_bit(unsigned char inbit)
    {
      unsigned char outbit;
      
      outbit = ~(inbit ^ d_shift_register ^ (d_shift_register >> 17) ^ (d_counter == 0x1f)) & 1;

      if (((d_shift_register >> 19) ^ (d_shift_register >> 11)) & 1) {
	d_counter = 0;
      }
      else {
	d_counter++;
	d_counter &= 0x1f;
      }

      d_shift_register >>= 1;
      d_shift_register |= (inbit & 1) << 19;

      return outbit;
    }

  } /* namespace satellites */
} /* namespace gr */

