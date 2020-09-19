/* -*- c++ -*- */
/*
 * Copyright 2017 Glenn Richardson <glenn@spacequest.com>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_VARLEN_PACKET_FRAMER_IMPL_H
#define INCLUDED_VARLEN_PACKET_FRAMER_IMPL_H

#include <pmt/pmt.h>
#include <satellites/varlen_packet_framer.h>

//#define VLPF_DEBUG_TIMING

namespace gr {
namespace satellites {
class varlen_packet_framer_impl : public varlen_packet_framer
{
private:
    int d_header_length;              // size of packet length field in bits
    bool d_use_golay;                 // decode golay packet length
    std::vector<uint8_t> d_sync_word; // option ASM
    endianness_t d_endianness;        // header endianness
    pmt::pmt_t d_packet_tag;          // packet length tag
    int d_ninput_items_required;

#ifdef VLPF_DEBUG_TIMING
    std::time_t d_last_debug1;
    std::time_t d_last_debug2;
    std::time_t d_start_time;
#endif


public:
    varlen_packet_framer_impl(const std::string& packet_key,
                              int length_field_size,
                              endianness_t endianness,
                              bool use_golay,
                              const std::vector<uint8_t> sync_word);

    ~varlen_packet_framer_impl();

    void forecast(int noutput_items, gr_vector_int& ninput_items_required);

    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items);
};

} // namespace satellites
} // namespace gr

#endif
