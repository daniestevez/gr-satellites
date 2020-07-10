/* -*- c++ -*- */
/*
 * Copyright 2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_NRZI_ENCODE_IMPL_H
#define INCLUDED_SATELLITES_NRZI_ENCODE_IMPL_H

#include <satellites/nrzi_encode.h>

namespace gr {
  namespace satellites {

    class nrzi_encode_impl : public nrzi_encode
    {
     private:
      uint8_t d_last;

     public:
      nrzi_encode_impl();
      ~nrzi_encode_impl();

      // Where all the action really happens
      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_NRZI_ENCODE_IMPL_H */

