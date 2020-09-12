/* -*- c++ -*- */
/*
 * Copyright 2016 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_DECODE_RS_IMPL_H
#define INCLUDED_SATELLITES_DECODE_RS_IMPL_H

#include <satellites/decode_rs.h>

#include <array>

#include "rs.h"

namespace gr {
  namespace satellites {

    class decode_rs_impl : public decode_rs
    {
     private:
      bool d_verbose;
      int d_basis;
      std::array<uint8_t, MAX_FRAME_LEN> d_data;

     public:
      decode_rs_impl(bool verbose, int basis);
      ~decode_rs_impl();

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

#endif /* INCLUDED_SATELLITES_DECODE_RS_IMPL_H */

