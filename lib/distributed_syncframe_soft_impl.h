/* -*- c++ -*- */
/*
 * Copyright 2019 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_DISTRIBUTED_SYNCFRAME_SOFT_IMPL_H
#define INCLUDED_SATELLITES_DISTRIBUTED_SYNCFRAME_SOFT_IMPL_H

#include <satellites/distributed_syncframe_soft.h>

namespace gr {
  namespace satellites {

    class distributed_syncframe_soft_impl : public distributed_syncframe_soft
    {
     private:
      int d_threshold;
      int d_synclen;
      int d_step;
      uint8_t *d_syncword;
            
     public:
      distributed_syncframe_soft_impl(int threshold, const std::string& syncword, int step);
      ~distributed_syncframe_soft_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_DISTRIBUTED_SYNCFRAME_SOFT_IMPL_H */
