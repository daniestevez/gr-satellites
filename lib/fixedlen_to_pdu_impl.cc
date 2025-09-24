/* -*- c++ -*- */
/*
 * Copyright 2022,2025 Daniel Estevez <daniel@destevez.net>
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

fixedlen_to_pdu::sptr fixedlen_to_pdu::make(types::vector_type type,
                                            const std::string& syncword_tag,
                                            size_t packet_len,
                                            bool pack,
                                            const std::string& packet_length_tag_key)
{
    return gnuradio::make_block_sptr<fixedlen_to_pdu_impl>(
        type, syncword_tag, packet_len, pack, packet_length_tag_key);
}

fixedlen_to_pdu_impl::fixedlen_to_pdu_impl(types::vector_type type,
                                           const std::string& syncword_tag,
                                           size_t packet_len,
                                           bool pack,
                                           const std::string& packet_length_tag_key)
    : gr::sync_block("fixedlen_to_pdu",
                     gr::io_signature::make(1, 1, pdu::itemsize(type)),
                     gr::io_signature::make(0, 0, 0)),
      d_type(type),
      d_itemsize(pdu::itemsize(d_type)),
      d_pack(pack),
      d_packetlen(packet_len),
      d_syncword_tag(pmt::mp(syncword_tag)),
      d_packet_length_tag(packet_length_tag_key.empty()
                              ? std::nullopt
                              : std::optional(pmt::mp(packet_length_tag_key))),
      d_history((packet_len - 1) * d_itemsize),
      d_packet(packet_len * d_itemsize)
{
    if (pack && type != types::byte_t) {
        throw std::runtime_error("pack can only be used with byte_t");
    }
    if (pack && packet_len % 8 != 0) {
        throw std::runtime_error("when using pack, packet_len must be a multiple of 8");
    }
    message_port_register_out(msgport_names::pdus());
}

fixedlen_to_pdu_impl::~fixedlen_to_pdu_impl() {}

int fixedlen_to_pdu_impl::work(int noutput_items,
                               gr_vector_const_void_star& input_items,
                               gr_vector_void_star& output_items)
{
    auto in = static_cast<const uint8_t*>(input_items[0]);

    std::vector<tag_t> tags;
    get_tags_in_window(tags, 0, 0, noutput_items, d_syncword_tag);
    for (const auto& tag : tags) {
        packet_info info;
        info.offset = tag.offset;
        info.length = d_packetlen;
        if (d_packet_length_tag.has_value()) {
            std::vector<tag_t> tags;
            get_tags_in_range(tags, 0, tag.offset, tag.offset + 1, *d_packet_length_tag);
            if (!tags.empty()) {
                const auto& value = tags[0].value;
                uint64_t length;
                if (pmt::is_uint64(value)) {
                    length = pmt::to_uint64(value);
                } else {
                    length = pmt::to_long(value);
                }
                if (length > d_packetlen) {
                    d_logger->warn("length tag value {} larger than max length {}; "
                                   "clamping to max length",
                                   length,
                                   d_packetlen);
                    info.length = d_packetlen;
                } else {
                    info.length = length;
                }
            }
        }
        d_packet_infos.push_back(info);
    }

    const auto nitems = nitems_read(0);
    d_new_packet_infos.clear();
    for (const auto& info : d_packet_infos) {
        if (info.offset + info.length <= nitems + noutput_items) {
            // Packet ends in current input_items buffer
            if (info.offset >= nitems) {
                // Packet doesn't use history
                std::memcpy(d_packet.data(),
                            &in[(info.offset - nitems) * d_itemsize],
                            info.length * d_itemsize);
            } else if (d_write_ptr_item + info.offset >= nitems) {
                // Packet starts before the write pointer
                const size_t start =
                    (d_write_ptr_item + info.offset - nitems) * d_itemsize;
                const size_t len =
                    std::min(d_write_ptr_byte - start, info.length * d_itemsize);
                std::memcpy(d_packet.data(), &d_history[start], len);
                const size_t remain = info.length * d_itemsize - len;
                if (remain > 0) {
                    std::memcpy(&d_packet[len], &in[0], remain);
                }
            } else {
                // Packet starts after the write pointer
                const size_t start =
                    (d_write_ptr_item + info.offset + d_packetlen - 1 - nitems) *
                    d_itemsize;
                const size_t len =
                    std::min(d_history.size() - start, info.length * d_itemsize);
                std::memcpy(d_packet.data(), &d_history[start], len);
                size_t remain = info.length * d_itemsize - len;
                if (remain > 0) {
                    const size_t len2 = std::min(d_write_ptr_byte, remain);
                    std::memcpy(&d_packet[len], d_history.data(), len2);
                    remain -= len2;
                    if (remain) {
                        std::memcpy(&d_packet[len + len2], &in[0], remain);
                    }
                }
            }

            const size_t pdu_items = d_pack ? info.length / 8 : info.length;
            if (d_pack) {
                if (info.length % 8 != 0) {
                    d_logger->warn("packet size {} is not a multiple of 8 bits, "
                                   "discarding remaining bits while packing");
                }
                pack_packet(pdu_items);
            }
            message_port_pub(
                msgport_names::pdus(),
                pmt::cons(pmt::PMT_NIL,
                          pdu::make_pdu_vector(d_type, d_packet.data(), pdu_items)));
        } else {
            // End of packet not yet available. Save for next run
            d_new_packet_infos.push_back(info);
        }
    }
    d_packet_infos.swap(d_new_packet_infos);

    update_history(in, noutput_items);
    return noutput_items;
}

void fixedlen_to_pdu_impl::pack_packet(size_t size_bytes)
{
    for (size_t j = 0; j < size_bytes; ++j) {
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
        start = (noutput_items - history_items) * d_itemsize;
        len = d_history.size();
        len_items = history_items;
    } else {
        start = 0;
        len = noutput_items * d_itemsize;
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
