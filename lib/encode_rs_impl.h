/* -*- c++ -*- */
/*
 * Copyright 2018 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_ENCODE_RS_IMPL_H
#define INCLUDED_SATELLITES_ENCODE_RS_IMPL_H

#include <satellites/encode_rs.h>

namespace gr {
  namespace satellites {

    class encode_rs_impl : public encode_rs
    {
     private:
      int d_basis;

     public:
      encode_rs_impl(int basis);
      ~encode_rs_impl();

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

#endif /* INCLUDED_SATELLITES_ENCODE_RS_IMPL_H */

