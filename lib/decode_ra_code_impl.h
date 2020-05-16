/* -*- c++ -*- */
/*
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_DECODE_RA_CODE_IMPL_H
#define INCLUDED_SATELLITES_DECODE_RA_CODE_IMPL_H

#include <satellites/decode_ra_code.h>

extern "C" {
#include "radecoder/ra_config.h"
}

namespace gr {
  namespace satellites {

    class decode_ra_code_impl : public decode_ra_code
    {
     private:
      int d_size;
      struct ra_context *d_ra_context;
      
     public:
      decode_ra_code_impl(int size);
      ~decode_ra_code_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

      void msg_handler(pmt::pmt_t pmt_msg);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_DECODE_RA_CODE_IMPL_H */

