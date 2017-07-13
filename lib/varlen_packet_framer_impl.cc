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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <cstdio>
#include <iostream>
#include "varlen_packet_framer_impl.h"

extern "C" {
#include <fec.h>
#include "golay24.h"
}

namespace gr {
  namespace satellites {

    varlen_packet_framer::sptr
    varlen_packet_framer::make(const std::string &packet_key,
                               int length_field_size,
                               endianness_t endianness,
                               bool use_golay,
                               const std::vector<uint8_t> sync_word )
    {
      return gnuradio::get_initial_sptr
        (new varlen_packet_framer_impl(packet_key,
                                       length_field_size,
                                       endianness,
                                       use_golay,
                                       sync_word));
    }

    varlen_packet_framer_impl::varlen_packet_framer_impl(
        const std::string &packet_key,
        int length_field_size,
        endianness_t endianness,
        bool use_golay,
        const std::vector<uint8_t> sync_word) : gr::block("varlen_packet_framer",
                        io_signature::make(1, 1, sizeof(char)),
                        io_signature::make(1, 1, sizeof(char))),
      d_header_length(length_field_size),
      d_endianness(endianness),
      d_use_golay(use_golay),
      d_sync_word(sync_word)
    {
      d_packet_tag = pmt::string_to_symbol(packet_key);

      set_tag_propagation_policy(TPP_DONT);

      for (int ii; ii<d_sync_word.size(); ii++) {
        d_sync_word.at(ii) = d_sync_word[ii] & 0x01;
      }

      d_header_length = ((d_header_length+7)/8)*8;
      d_header_length = std::max(32, std::min(8, d_header_length));
      
      if (d_use_golay)
          d_header_length = 24;
    }


    varlen_packet_framer_impl::~varlen_packet_framer_impl()
    {
    }

    int
    varlen_packet_framer_impl::general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];
      int packet_len = 0;
      std::vector<tag_t> tags;

      uint32_t header = 0;
      unsigned int asm_len = d_sync_word.size();

      // find the next packet_tag
      get_tags_in_range(tags, 0, nitems_read(0),
                        nitems_read(0) + ninput_items[0],
                        d_packet_tag);
      if (tags.size() > 0) {
        // check for packet size
        packet_len = to_uint64(tags[0].value);

        if ((ninput_items[0] >= tags[0].offset - nitems_read(0) + packet_len) &&
            (noutput_items >= packet_len + d_header_length + asm_len)) {

          // copy the option sync word
          if (asm_len > 0) {
            memcpy(out, (const void *) &d_sync_word[0], asm_len);
            out += asm_len;
          }

          // create the length field header
          header = packet_len / 8;
          if (d_use_golay) {
            encode_golay24(&header);
          }

          // copy header
          if (d_endianness == GR_MSB_FIRST) {
            for (int ii=0; ii<d_header_length; ii++) {
              out[ii] = (header>>(d_header_length-ii-1)) & 0x01;
            }
          } else {
            for (int ii=0; ii<d_header_length; ii++) {
              out[ii] = (header>>ii) & 0x01;
            }

          }

          // copy data and tag
          memcpy(&out[d_header_length], in, packet_len);
          add_item_tag(0, nitems_written(0),
              d_packet_tag, pmt::from_long(packet_len + d_header_length + asm_len),
              alias_pmt());
          consume_each(packet_len);

          return packet_len + d_header_length + asm_len;
        }
      }
      return 0;
    }




  } /* namespace satellites */
} /* namespace gr */
