/* -*- c++ -*- */
/*
 * Copyright 2022-2023,2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "nanocom_golay_decode_length_impl.h"
#include <gnuradio/io_signature.h>
#include <algorithm>
#include <cstdint>

extern "C" {
#include "golay24.h"
}

namespace gr {
namespace satellites {

nanocom_golay_decode_length::sptr
nanocom_golay_decode_length::make(const std::string& golay_start_tag_key,
                                  const std::string& length_tag_key)
{
    return gnuradio::make_block_sptr<nanocom_golay_decode_length_impl>(
        golay_start_tag_key, length_tag_key);
}


nanocom_golay_decode_length_impl::nanocom_golay_decode_length_impl(
    const std::string& golay_start_tag_key, const std::string& length_tag_key)
    : gr::sync_block("nanocom_golay_decode_length",
                     gr::io_signature::make(1, 1, sizeof(uint8_t)),
                     gr::io_signature::make(1, 1, sizeof(uint8_t))),
      d_golay_start_tag_key(pmt::mp(golay_start_tag_key)),
      d_length_tag_key(pmt::mp(length_tag_key))
{
    set_history(k_golay_N);
    set_tag_propagation_policy(TPP_DONT);
}

nanocom_golay_decode_length_impl::~nanocom_golay_decode_length_impl() {}

int nanocom_golay_decode_length_impl::work(int noutput_items,
                                           gr_vector_const_void_star& input_items,
                                           gr_vector_void_star& output_items)
{
    auto in = static_cast<const uint8_t*>(input_items[0]);
    auto out = static_cast<uint8_t*>(output_items[0]);

    const int delay = k_golay_N - 1;
    const int64_t nitems = nitems_read(0);
    const uint64_t start = std::max(nitems - delay, static_cast<int64_t>(0));
    const uint64_t end =
        std::max(nitems + noutput_items - delay, static_cast<int64_t>(0));
    std::vector<gr::tag_t> tags;
    get_tags_in_range(tags, 0, start, end, d_golay_start_tag_key);
    for (const auto& tag : tags) {
        const int offset = tag.offset - nitems + delay;
        uint32_t golay_field = 0;
        for (int j = 0; j < k_golay_N; ++j) {
            golay_field = (golay_field << 1) | (in[offset + j] & 1);
        }
        auto golay_res = decode_golay24(&golay_field);
        if (golay_res < 0) {
            d_logger->info("Golay decode failed");
        }
        auto frame_len = golay_field & 0xff;
        auto frame_len_bits = 8 * frame_len + k_golay_N;
        add_item_tag(
            0, tag.offset + delay, d_length_tag_key, pmt::from_uint64(frame_len_bits));
    }

    std::copy_n(in, noutput_items, out);
    // propagate tags, applying 'delay' to them
    get_tags_in_range(tags, 0, nitems, nitems + noutput_items);
    for (const auto& tag : tags) {
        add_item_tag(0, tag.offset + delay, tag.key, tag.value);
    }

    return noutput_items;
}

} /* namespace satellites */
} /* namespace gr */
