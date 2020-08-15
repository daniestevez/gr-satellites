/* -*- c++ -*- */
/* 
 * Copyright 2016,2020 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_AX100_DECODE_IMPL_H
#define INCLUDED_SATELLITES_AX100_DECODE_IMPL_H

#include <satellites/ax100_decode.h>

#include <array>

namespace gr {
  namespace satellites {

    class ax100_decode_impl : public ax100_decode
    {
     private:
      std::array<uint8_t, 256> d_data;
      const bool d_verbose;

     public:
      ax100_decode_impl(bool verbose);
      ~ax100_decode_impl();

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

#endif /* INCLUDED_SATELLITES_AX100_DECODE_IMPL_H */

