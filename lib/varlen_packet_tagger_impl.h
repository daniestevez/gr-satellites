/* -*- c++ -*- */
/*
 * Copyright 2017 Glenn Richardson <glenn@spacequest.com> 
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>
 */

#ifndef INCLUDED_VARLEN_PACKET_TAGGER_IMPL_H
#define INCLUDED_VARLEN_PACKET_TAGGER_IMPL_H

#include <satellites/varlen_packet_tagger.h>
#include <pmt/pmt.h>


namespace gr {
  namespace satellites {
    class varlen_packet_tagger_impl :
      public varlen_packet_tagger
    {
    private:      
      int d_header_length; // bit size of packet length field
      int d_mtu; // maximum packet size in bits
      bool d_use_golay; // decode golay packet length
      endianness_t d_endianness; // header endianness

      pmt::pmt_t d_sync_tag; // marker tag on input for start of packet
      pmt::pmt_t d_packet_tag; // packet_len tag for output stream

      bool d_have_sync; // interal state
      int d_ninput_items_required; // forecast

      int bits2len(const unsigned char *in);

    public:
      varlen_packet_tagger_impl(const std::string &sync_key,
                                  const std::string &packet_key,
                                  int length_field_size,
                                  int max_packet_size,
                                  endianness_t endianness,
                                  bool use_golay);
      ~varlen_packet_tagger_impl();

      void forecast(int noutput_items, gr_vector_int &ninput_itens_required);

      int general_work(int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items);      
    };

  } // namespace satellites
} // namespace gr

#endif

