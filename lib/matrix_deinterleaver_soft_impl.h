/* -*- c++ -*- */
/*
 * Copyright 2019 Daniel Estevez <daniel@destevez.net>.
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

#ifndef INCLUDED_SATELLITES_MATRIX_DEINTERLEAVER_SOFT_IMPL_H
#define INCLUDED_SATELLITES_MATRIX_DEINTERLEAVER_SOFT_IMPL_H

#include <satellites/matrix_deinterleaver_soft.h>

namespace gr {
  namespace satellites {

    class matrix_deinterleaver_soft_impl : public matrix_deinterleaver_soft
    {
     private:
      int d_rows;
      int d_cols;
      int d_output_size;
      int d_output_skip;

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

