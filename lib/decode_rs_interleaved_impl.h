/* -*- c++ -*- */
/*
 * Copyright 2019-2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_DECODE_RS_INTERLEAVED_IMPL_H
#define INCLUDED_SATELLITES_DECODE_RS_INTERLEAVED_IMPL_H

#include <satellites/decode_rs_interleaved.h>

#include <array>
#include <vector>

#include "rs.h"

namespace gr {
  namespace satellites {

    class decode_rs_interleaved_impl : public decode_rs_interleaved
    {
     private:
      const bool d_verbose;
      const int d_basis;
      const size_t d_codewords;
      std::array<uint8_t, MAX_FRAME_LEN> d_codeword;
      std::vector<uint8_t> d_out;

     public:
      decode_rs_interleaved_impl(bool verbose, int basis, int codewords);
      ~decode_rs_interleaved_impl();

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

#endif /* INCLUDED_SATELLITES_DECODE_RS_INTERLEAVED_IMPL_H */

