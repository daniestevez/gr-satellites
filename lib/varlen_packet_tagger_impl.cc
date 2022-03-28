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

#include "varlen_packet_tagger_impl.h"
#include <gnuradio/io_signature.h>
#include <cstdio>
#include <iostream>
#include <boost/format.hpp>
extern "C" {
#include "golay24.h"
#include "libfec/fec.h"
}

namespace gr {
namespace satellites {

varlen_packet_tagger::sptr varlen_packet_tagger::make(const std::string& sync_key,
                                                      const std::string& packet_key,
                                                      int length_field_size,
                                                      int max_packet_size,
                                                      endianness_t endianness,
                                                      bool use_golay)
{
    return gnuradio::get_initial_sptr(new varlen_packet_tagger_impl(
        sync_key, packet_key, length_field_size, max_packet_size, endianness, use_golay));
}

varlen_packet_tagger_impl::varlen_packet_tagger_impl(const std::string& sync_key,
                                                     const std::string& packet_key,
                                                     int length_field_size,
                                                     int max_packet_size,
                                                     endianness_t endianness,
                                                     bool use_golay)
    : gr::block("varlen_packet_tagger",
                io_signature::make(1, 1, sizeof(char)),
                io_signature::make(1, 1, sizeof(char))),
      d_header_length(length_field_size),
      d_mtu(max_packet_size),
      d_use_golay(use_golay),
      d_endianness(endianness),
      d_have_sync(false)
{
    d_sync_tag = pmt::string_to_symbol(sync_key);
    d_packet_tag = pmt::string_to_symbol(packet_key);
    d_ninput_items_required = d_header_length + 1;

    set_tag_propagation_policy(TPP_DONT);

    if (d_use_golay)
        d_header_length = 24;
}


varlen_packet_tagger_impl::~varlen_packet_tagger_impl() {}

int varlen_packet_tagger_impl::bits2len(const unsigned char* in)
{
    // extract the packet length from the header
    int ret = 0;
    if (d_endianness == GR_MSB_FIRST) {
        for (int i = 0; i < d_header_length; i++) {
            ret = (ret << 0x01) + in[i];
        }
    } else {
        for (int i = d_header_length - 1; i >= 0; i--) {
            ret = (ret << 0x01) + in[i];
        }
    }
    return ret;
}

void varlen_packet_tagger_impl::forecast(int noutput_items,
                                         gr_vector_int& ninput_items_required)
{
    unsigned ninputs = ninput_items_required.size();
    for (unsigned i = 0; i < ninputs; i++)
        ninput_items_required[i] = d_ninput_items_required;
}

int varlen_packet_tagger_impl::general_work(int noutput_items,
                                            gr_vector_int& ninput_items,
                                            gr_vector_const_void_star& input_items,
                                            gr_vector_void_star& output_items)
{
    const unsigned char* in = (const unsigned char*)input_items[0];
    unsigned char* out = (unsigned char*)output_items[0];
    int packet_len = 0;
    std::vector<tag_t> tags;

    uint32_t golay_field;
    int golay_res;

    if (d_have_sync) {
        if (d_header_length > ninput_items[0]) {
            // not enough data yet
            return 0;
        }

        if (d_use_golay) {
            golay_field = bits2len(in);
            golay_res = decode_golay24(&golay_field);
            if (golay_res >= 0) {
                packet_len = 8 * (0xFFF & golay_field);
            } else {
                GR_LOG_WARN(d_debug_logger, "Golay decode failed.");
                d_have_sync = false;
                consume_each(1); // skip ahead
                return 0;
            }

        } else {
            packet_len = 8 * bits2len(in);
        }

        if (packet_len > d_mtu) {
            GR_LOG_WARN(d_debug_logger,
                        boost::format("Packet length %d > mtu %d.") % packet_len % d_mtu);
            d_have_sync = false;
            consume_each(1); // skip ahead
            return 0;
        }

        d_ninput_items_required = d_header_length + packet_len;

        if (noutput_items < packet_len) {
            set_min_noutput_items(packet_len);
            return 0;
        }
        set_min_noutput_items(1);

        if (ninput_items[0] >= packet_len + d_header_length) {

            if (d_use_golay) {
                GR_LOG_DEBUG(d_debug_logger,
                             boost::format("Header: 0x%06x, Len: %d") %
                                 (0xFFFFFF & golay_field) % (0xFFF & packet_len));
                if (golay_res >= 0) {
                    GR_LOG_DEBUG(d_debug_logger,
                                 boost::format("Golay decoded. Errors: %d, Length: %d") %
                                     golay_res % packet_len);
                }
            }

            memcpy(out, &in[d_header_length], packet_len);
            add_item_tag(0,
                         nitems_written(0),
                         d_packet_tag,
                         pmt::from_long(packet_len),
                         alias_pmt());
            d_have_sync = false;

            // consuming only the header allows for
            // ... multiple syncs per 'packet',
            // ... in case the sync was incorrectly tagged
            consume_each(d_header_length);
            d_ninput_items_required = d_header_length + 1;
            return packet_len;
        }

    } else {
        // find the next sync tag, drop all other data
        get_tags_in_range(
            tags, 0, nitems_read(0), nitems_read(0) + ninput_items[0], d_sync_tag);
        if (tags.size() > 0) {
            d_have_sync = true;
            consume_each(tags[0].offset - nitems_read(0));
        } else {
            consume_each(ninput_items[0]);
        }
    }
    return 0;
}

} /* namespace satellites */
} /* namespace gr */
