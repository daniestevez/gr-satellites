/* -*- c++ -*- */
/*
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_AO40_RS_DECODER_IMPL_H
#define INCLUDED_SATELLITES_AO40_RS_DECODER_IMPL_H

#include <satellites/ao40_rs_decoder.h>

namespace gr {
  namespace satellites {

    class ao40_rs_decoder_impl : public ao40_rs_decoder
    {
     private:
      bool d_verbose;

     public:
      ao40_rs_decoder_impl(bool verbose);
      ~ao40_rs_decoder_impl();

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

#endif /* INCLUDED_SATELLITES_AO40_RS_DECODER_IMPL_H */

