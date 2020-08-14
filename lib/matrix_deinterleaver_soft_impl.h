/* -*- c++ -*- */
/*
 * Copyright 2019 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_MATRIX_DEINTERLEAVER_SOFT_IMPL_H
#define INCLUDED_SATELLITES_MATRIX_DEINTERLEAVER_SOFT_IMPL_H

#include <satellites/matrix_deinterleaver_soft.h>

#include <vector>

namespace gr {
  namespace satellites {

    class matrix_deinterleaver_soft_impl : public matrix_deinterleaver_soft
    {
     private:
      const int d_rows;
      const int d_cols;
      const int d_output_size;
      const int d_output_skip;
      std::vector<float> d_out;

     public:
      matrix_deinterleaver_soft_impl(int rows, int cols, int output_size, int output_skip);
      ~matrix_deinterleaver_soft_impl();

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

#endif /* INCLUDED_SATELLITES_MATRIX_DEINTERLEAVER_SOFT_IMPL_H */

