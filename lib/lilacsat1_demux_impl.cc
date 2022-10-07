/* -*- c++ -*- */
/*
 * Copyright 2017,2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <cassert>
#include <cstring>
#include <vector>

#include "lilacsat1_demux_impl.h"
#include <gnuradio/io_signature.h>

#define CODEC2_FRAME_LEN 7
#define CHUNK_LEN 24
#define BITS_PER_BYTE 8
#define PACKET_LEN 116
#define HEADER_LEN 4
#define FRAME_LEN (5 * (CHUNK_LEN - CODEC2_FRAME_LEN) - HEADER_LEN)

namespace gr {
namespace satellites {

lilacsat1_demux::sptr lilacsat1_demux::make(std::string tag)
{
    return gnuradio::make_block_sptr<lilacsat1_demux_impl>(tag);
}

/*
 * The private constructor
 */
lilacsat1_demux_impl::lilacsat1_demux_impl(std::string tag)
    : gr::sync_block("lilacsat1_demux",
                     gr::io_signature::make(1, 1, sizeof(uint8_t)),
                     gr::io_signature::make(0, 0, 0)),
      d_position(-1),
      d_tag(pmt::string_to_symbol(tag))
{
    d_frame.fill(0);
    d_codec2.fill(0);

    message_port_register_out(pmt::mp("frame"));
    message_port_register_out(pmt::mp("codec2"));
}

/*
 * Our virtual destructor.
 */
lilacsat1_demux_impl::~lilacsat1_demux_impl() {}

int lilacsat1_demux_impl::work(int noutput_items,
                               gr_vector_const_void_star& input_items,
                               gr_vector_void_star& output_items)
{
    const uint8_t* in = (const uint8_t*)input_items[0];
    std::vector<tag_t> tags;

    for (int i = 0; i < noutput_items; ++i) {
        get_tags_in_window(tags, 0, i, i + 1, d_tag);

        if (!tags.empty()) {
            d_position = 0;
        }

        if (d_position == d_packet_len * d_bits_per_byte) {
            d_position = -1;

            message_port_pub(
                pmt::mp("frame"),
                pmt::cons(pmt::PMT_NIL,
                          pmt::init_u8vector(d_frame.size(), d_frame.data())));
            d_frame.fill(0);
        }

        if (d_position == -1)
            continue;

        auto base = d_position / d_bits_per_byte + d_header_len;
        auto bit = d_bits_per_byte - 1 - d_position % d_bits_per_byte;
        auto idx = base % d_chunk_len;
        if (idx >= d_chunk_len - d_codec2_frame_len) {
            auto byte = idx - (d_chunk_len - d_codec2_frame_len);
            d_codec2.at(byte) |= (in[i] & 1) << bit;

            if ((byte == d_codec2.size() - 1) && (bit == 0)) {
                message_port_pub(
                    pmt::mp("codec2"),
                    pmt::cons(pmt::PMT_NIL,
                              pmt::init_u8vector(d_codec2.size(), d_codec2.data())));
                d_codec2.fill(0);
            }
        } else if (idx < d_chunk_len - d_codec2_frame_len) {
            auto byte = (base / d_chunk_len) * (d_chunk_len - d_codec2_frame_len) + idx -
                        d_header_len;
            d_frame.at(byte) |= (in[i] & 1) << bit;
        }

        ++d_position;
    }

    return noutput_items;
}

} /* namespace satellites */
} /* namespace gr */
