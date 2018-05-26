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

#ifndef INCLUDED_SATELLITES_DESCRAMBLER308_IMPL_H
#define INCLUDED_SATELLITES_DESCRAMBLER308_IMPL_H

#include <stdint.h>

#include <satellites/descrambler308.h>

namespace gr {
  namespace satellites {

    class descrambler308_impl : public descrambler308
    {
     private:
      uint32_t d_counter;
      uint32_t d_shift_register;
      unsigned char d_scramble_bit(unsigned char inbit);

     public:
      descrambler308_impl();
      ~descrambler308_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_DESCRAMBLER308_IMPL_H */

