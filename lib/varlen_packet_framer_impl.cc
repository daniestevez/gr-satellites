/* -*- c++ -*- */
/*
 * Copyright 2017 Glenn Richardson <glenn@spacequest.com>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <cstdio>
#include <ctime>
#include <iostream>
#include "varlen_packet_framer_impl.h"

extern "C" {
#include "libfec/fec.h"
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
      d_sync_word(sync_word),
      d_ninput_items_required(1)
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

#ifdef VLPF_DEBUG_TIMING
      d_last_debug1 = std::time(NULL);
      d_last_debug2 = std::time(NULL);
      d_start_time = std::time(NULL);
#endif
    }


    varlen_packet_framer_impl::~varlen_packet_framer_impl()
    {
    }

    void
    varlen_packet_framer_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
    {
      unsigned ninputs = ninput_items_required.size();
      for(unsigned i = 0; i < ninputs; i++)
        ninput_items_required[i] = d_ninput_items_required;
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

        if (noutput_items < packet_len + d_header_length + asm_len) {
          set_min_noutput_items(packet_len + d_header_length + asm_len);
#ifdef VLPF_DEBUG_TIMING
          if (std::time(NULL) - d_last_debug1 > 1) {
            std::cout << (std::time(NULL) - d_start_time) 
                      << "nouput:" << noutput_items 
                      << " req:" << (packet_len+d_header_length + asm_len) 
                      << std::endl;
            d_last_debug1 = std::time(NULL);
          }
#endif
          return 0;
        }
        set_min_noutput_items(1);

        d_ninput_items_required = tags[0].offset - nitems_read(0) + packet_len;
        if (ninput_items[0] >= d_ninput_items_required) {
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

#ifdef VLPF_DEBUG_TIMING
          std::cout << (std::time(NULL) - d_start_time) 
                    << ":\tASM Framed @ " << nitems_written(0) 
                    << " len " << packet_len 
                    << std::endl;
          std::cout << "\tread: " << nitems_read(0)
                    << "\tini:  " << ninput_items[0]
                    << "\touti: " << noutput_items
                    << std::endl;
#endif
          GR_LOG_DEBUG(d_debug_logger,
                       boost::format("%d byte packet output @ %ld") \
                       % packet_len % nitems_written(0));
          d_ninput_items_required = 1;//d_header_length + asm_len + 1; // abs min
          return packet_len + d_header_length + asm_len;
        }
        else {
#ifdef VLPF_DEBUG_TIMING
          if (std::time(NULL) - d_last_debug2 >= 1) {
            std::cout << (std::time(NULL) - d_start_time) 
                      << ":\tASM not enough input:" << ninput_items[0]
                      << " req:" << d_ninput_items_required << std::endl;
            d_last_debug2 = std::time(NULL);
          }
#endif
        }
      }
      return 0;
    }


  } /* namespace satellites */
} /* namespace gr */
