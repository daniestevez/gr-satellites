/* -*- c++ -*- */
/*
 * Copyright 2022 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#include "fixedlen_to_pdu_impl.h"
#include <gnuradio/io_signature.h>
#include <cstring>
#include <stdexcept>

namespace gr {
namespace satellites {

fixedlen_to_pdu::sptr fixedlen_to_pdu::make(blocks::pdu::vector_type type,
                                            const std::string& syncword_tag,
                                            size_t packet_len,
                                            bool pack)
{
    return gnuradio::make_block_sptr<fixedlen_to_pdu_impl>(
        type, syncword_tag, packet_len, pack);
}

fixedlen_to_pdu_impl::fixedlen_to_pdu_impl(blocks::pdu::vector_type type,
                                           const std::string& syncword_tag,
                                           size_t packet_len,
                                           bool pack)
    : gr::sync_block("fixedlen_to_pdu",
                     gr::io_signature::make(1, 1, blocks::pdu::itemsize(type)),
                     gr::io_signature::make(0, 0, 0)),
      d_type(type),
      d_pack(pack),
      d_packetlen(packet_len),
      d_packet_nbytes(packet_len * blocks::pdu::itemsize(type)),
      d_pdu_items(pack ? packet_len / 8 : packet_len),
      d_syncword_tag(pmt::mp(syncword_tag)),
      d_history((packet_len - 1) * blocks::pdu::itemsize(type)),
      d_write_ptr_item(0),
      d_write_ptr_byte(0),
      d_packet(packet_len * blocks::pdu::itemsize(type)),
      d_tag_offsets(0)
{
    if (pack && type != blocks::pdu::byte_t) {
        throw std::runtime_error("pack can only be used with byte_t");
    }
    if (pack && packet_len % 8 != 0) {
        throw std::runtime_error("when using pack, packet_len must be a multiple of 8");
    }
    message_port_register_out(blocks::pdu::pdu_port_id());
}

fixedlen_to_pdu_impl::~fixedlen_to_pdu_impl() {}

int fixedlen_to_pdu_impl::work(int noutput_items,
                               gr_vector_const_void_star& input_items,
                               gr_vector_void_star& output_items)
{
    auto in = static_cast<const uint8_t*>(input_items[0]);

    get_tags_in_window(d_tags_in_window, 0, 0, noutput_items, d_syncword_tag);
    for (auto tag : d_tags_in_window) {
        d_tag_offsets.push_back(tag.offset);
    }

    std::list<uint64_t> tag_offsets_copy = d_tag_offsets;
    for (auto tag_offset : tag_offsets_copy) {
        if (tag_offset + d_packetlen <= nitems_read(0) + noutput_items) {
            // Packet ends in current input_items buffer
            if (tag_offset >= nitems_read(0)) {
                // Packet doesn't use history
                std::memcpy(
                    d_packet.data(),
                    &in[(tag_offset - nitems_read(0)) * blocks::pdu::itemsize(d_type)],
                    d_packet_nbytes);
            } else if (d_write_ptr_item + tag_offset >= nitems_read(0)) {
                // Packet starts before the write pointer
                size_t start = (d_write_ptr_item + tag_offset - nitems_read(0)) *
                               blocks::pdu::itemsize(d_type);
                size_t len = d_write_ptr_byte - start;
                std::memcpy(d_packet.data(), &d_history[start], len);
                std::memcpy(&d_packet[len], &in[0], d_packet_nbytes - len);
            } else {
                // Packet starts after the write pointer
                size_t start =
                    (d_write_ptr_item + tag_offset + d_packetlen - 1 - nitems_read(0)) *
                    blocks::pdu::itemsize(d_type);
                size_t len = d_history.size() - start;
                std::memcpy(d_packet.data(), &d_history[start], len);
                std::memcpy(&d_packet[len], d_history.data(), d_write_ptr_byte);
                std::memcpy(&d_packet[len + d_write_ptr_byte],
                            &in[0],
                            d_packet_nbytes - len - d_write_ptr_byte);
            }

            d_tag_offsets.erase(
                std::find(d_tag_offsets.begin(), d_tag_offsets.end(), tag_offset));
            if (d_pack) {
                pack_packet();
            }
            message_port_pub(blocks::pdu::pdu_port_id(),
                             pmt::cons(pmt::PMT_NIL,
                                       blocks::pdu::make_pdu_vector(
                                           d_type, d_packet.data(), d_pdu_items)));
        }
    }

    update_history(in, noutput_items);
    return noutput_items;
}

void fixedlen_to_pdu_impl::pack_packet()
{
    for (size_t j = 0; j < d_pdu_items; ++j) {
        uint8_t b = 0;
        for (int k = 0; k < 8; ++k) {
            b <<= 1;
            b |= d_packet[8 * j + k] & 1;
        }
        d_packet[j] = b;
    }
}

void fixedlen_to_pdu_impl::update_history(const uint8_t* in, int noutput_items)
{
    size_t start;
    size_t len;
    size_t len_items;
    const size_t history_items = d_packetlen - 1;
    if (static_cast<size_t>(noutput_items) > history_items) {
        start = (noutput_items - history_items) * blocks::pdu::itemsize(d_type);
        len = d_history.size();
        len_items = history_items;
    } else {
        start = 0;
        len = noutput_items * blocks::pdu::itemsize(d_type);
        len_items = noutput_items;
    }
    size_t len2;
    size_t len2_items;
    if (d_write_ptr_byte + len <= d_history.size()) {
        len2 = len;
        len2_items = len_items;
    } else {
        len2 = d_history.size() - d_write_ptr_byte;
        len2_items = history_items - d_write_ptr_item;
    }
    std::memcpy(&d_history[d_write_ptr_byte], &in[start], len2);
    if (len2 < len) {
        std::memcpy(&d_history[0], &in[start + len2], len - len2);
        d_write_ptr_byte = len - len2;
        d_write_ptr_item = len_items - len2_items;
    } else {
        d_write_ptr_byte += len;
        d_write_ptr_item += len_items;
        if (d_write_ptr_byte == d_history.size()) {
            d_write_ptr_byte = 0;
            d_write_ptr_item = 0;
        }
    }
}

} /* namespace satellites */
} /* namespace gr */
