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

#ifndef INCLUDED_VARLEN_PACKET_FRAMER_IMPL_H
#define INCLUDED_VARLEN_PACKET_FRAMER_IMPL_H

#include <satellites/varlen_packet_framer.h>
#include <pmt/pmt.h>


namespace gr {
  namespace satellites {
    class varlen_packet_framer_impl :
      public varlen_packet_framer
    {
    private:      
      int d_header_length; // size of packet length field in bits
      bool d_use_golay; // decode golay packet length
      std::vector<uint8_t> d_sync_word; // option ASM
      endianness_t d_endianness; // header endianness
      pmt::pmt_t d_packet_tag; // packet length tag



    public:
      varlen_packet_framer_impl(const std::string &packet_key,
                                int length_field_size,
                                endianness_t endianness,
                                bool use_golay,
                                const std::vector<uint8_t> sync_word);
      ~varlen_packet_framer_impl();

      int general_work(int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items);      
    };

  } // namespace satellites
} // namespace gr

#endif

