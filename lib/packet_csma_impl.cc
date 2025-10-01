/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "packet_csma_impl.h"
#include <gnuradio/io_signature.h>
#include <chrono>
#include <cstdint>
#include <stdexcept>
#include <thread>

namespace gr {
namespace satellites {

packet_csma::sptr packet_csma::make(size_t itemsize,
                                    bool back_to_back_priority,
                                    const std::string& len_tag_key)
{
    return gnuradio::make_block_sptr<packet_csma_impl>(
        itemsize, back_to_back_priority, len_tag_key);
}

packet_csma_impl::packet_csma_impl(size_t itemsize,
                                   bool back_to_back_priority,
                                   const std::string& len_tag_key)
    : gr::block("packet_csma",
                gr::io_signature::make(1, 1, itemsize),
                gr::io_signature::make(1, 1, itemsize)),
      d_itemsize(itemsize),
      d_len_tag_key(pmt::string_to_symbol(len_tag_key)),
      d_back_to_back_priority(back_to_back_priority)
{
    const auto in_port = pmt::string_to_symbol("carrier_sense");
    message_port_register_in(in_port);
    set_msg_handler(in_port,
                    [this](const pmt::pmt_t& msg) { this->handle_carrier_sense(msg); });
}

packet_csma_impl::~packet_csma_impl() {}

void packet_csma_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
{
    ninput_items_required[0] = noutput_items;
}

int packet_csma_impl::general_work(int noutput_items,
                                   gr_vector_int& ninput_items,
                                   gr_vector_const_void_star& input_items,
                                   gr_vector_void_star& output_items)
{
    auto in = static_cast<const uint8_t*>(input_items[0]);
    auto out = static_cast<uint8_t*>(output_items[0]);

    // if carrier sense is false, we can propagate all input to the output
    size_t num_propagate = std::min(noutput_items, ninput_items[0]);
    if (d_carrier_sense) {
        // if carrier sense is true, we need to check how much we are allowed to propagate
        if (d_remaining_items == 0) {
            // we had finished a packet in the previous work call, so the new
            // packet always must wait
            num_propagate = 0;
        } else if (d_back_to_back_priority) {
            // the input consists of back-to-back packets, so we can propagate
            // everything, so we do not need to do anything in this case
        } else {
            // only the current packet can be propagated
            num_propagate = std::min(num_propagate, d_remaining_items);
        }
    }

    // figure out how many items remain for the last packet we propagate
    const auto nitems = nitems_read(0);
    std::vector<gr::tag_t> tags;
    get_tags_in_range(tags, 0, nitems, nitems + num_propagate, d_len_tag_key);
    // we assume that the tags are sorted by index, which is guaranteed by GNU
    // Radio
    if (tags.size() > 0) {
        /// d_logger->warn("{} packets in current work", tags.size());
        // there are multiple packets beginning in the range that we will
        // propagate; consider only the last packet
        const auto& last_tag = tags.back();
        const auto length = pmt::to_uint64(last_tag.value);
        d_remaining_items = last_tag.offset + length - (nitems + num_propagate);
    } else {
        // there are no packets beginning in the range that we will propagate,
        // so subtract the length that we copy from the items that remain for
        // this packet
        if (num_propagate > d_remaining_items) {
            throw std::runtime_error(
                "[packet_csma] no packet_len tags seen but tried to propagate more than "
                "what remains of the current packet");
        }
        d_remaining_items -= num_propagate;
    }

    std::memcpy(out, in, d_itemsize * num_propagate);

    if (num_propagate == 0) {
        // We cannot produce anything in this call because we need to wait for
        // d_carrier_sense to become false. We need to sleep for a short while
        // here, because otherwise the scheduler would immediately call this
        // work() function again, wasting CPU.
        std::this_thread::sleep_for(std::chrono::microseconds(100));
    }

    consume(0, num_propagate);
    return num_propagate;
}

} /* namespace satellites */
} /* namespace gr */
