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

#include <array>

namespace gr {
  namespace satellites {

    class lilacsat1_demux_impl : public lilacsat1_demux
    {
     private:
      constexpr static size_t d_codec2_frame_len = 7;
      constexpr static size_t d_chunk_len = 24;
      constexpr static size_t d_bits_per_byte = 8;
      constexpr static size_t d_packet_len = 116;
      constexpr static size_t d_header_len = 4;
      constexpr static size_t d_frame_len =
	5 * (d_chunk_len - d_codec2_frame_len) - d_header_len;
      int d_position;
      pmt::pmt_t d_tag;
      std::array<uint8_t, d_frame_len> d_frame; // Current frame without codec2 bytes
      std::array<uint8_t, d_codec2_frame_len> d_codec2; // Current codec2 frame

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

