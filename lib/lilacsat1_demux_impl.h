/* -*- c++ -*- */
/*
 * Copyright 2017,2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_LILACSAT1_DEMUX_IMPL_H
#define INCLUDED_SATELLITES_LILACSAT1_DEMUX_IMPL_H

#include <string>
#include <pmt/pmt.h>

#include <satellites/lilacsat1_demux.h>

namespace gr {
  namespace satellites {

    class lilacsat1_demux_impl : public lilacsat1_demux
    {
     private:
      int d_position;
      pmt::pmt_t d_tag;
      uint8_t *d_frame; // Current frame without codec2 bytes
      uint8_t *d_codec2; // Current codec2 frame

     public:
      lilacsat1_demux_impl(std::string tag);
      ~lilacsat1_demux_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_LILACSAT1_DEMUX_IMPL_H */

