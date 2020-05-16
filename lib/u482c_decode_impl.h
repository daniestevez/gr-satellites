/* -*- c++ -*- */
/*
 * Copyright 2016 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_U482C_DECODE_IMPL_H
#define INCLUDED_SATELLITES_U428C_DECODE_IMPL_H

#include <satellites/u482c_decode.h>
#include <pmt/pmt.h>

#define RS_LEN 255
#define HEADER_LEN 3

namespace gr {
  namespace satellites {

    class u482c_decode_impl : public u482c_decode
    {
     private:
      bool d_verbose;
      char d_ccsds_sequence[RS_LEN];
      void *d_vp;
      int d_viterbi, d_scrambler, d_rs;
      
     public:
      u482c_decode_impl(bool verbose, int viterbi, int scrambler, int rs);
      ~u482c_decode_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

      void msg_handler (pmt::pmt_t pmt_msg);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_U482C_DECODE_IMPL_H */

