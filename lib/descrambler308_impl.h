/* -*- c++ -*- */
/*
 * Copyright 2018 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
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

