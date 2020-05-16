/* -*- c++ -*- */
/*
 * Copyright 2018 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_DECODE_RS_GENERAL_IMPL_H
#define INCLUDED_SATELLITES_DECODE_RS_GENERAL_IMPL_H

#include <satellites/decode_rs_general.h>

namespace gr {
  namespace satellites {

    class decode_rs_general_impl : public decode_rs_general
    {
     private:
      bool d_verbose;
      void *d_rs;
      int d_nroots;

     public:
      decode_rs_general_impl(int gfpoly, int fcr, int prim, int nroots, bool verbose);
      ~decode_rs_general_impl();

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

#endif /* INCLUDED_SATELLITES_DECODE_RS_GENERAL_IMPL_H */

