/* -*- c++ -*- */
/*
 * Copyright 2021 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "fixedlen_tagger_impl.h"
#include <gnuradio/io_signature.h>

#include <algorithm>

namespace gr {
namespace satellites {

fixedlen_tagger::sptr fixedlen_tagger::make(size_t sizeof_stream_item,
                                            const std::string& syncword_tag,
                                            const std::string& packetlen_tag,
                                            size_t packet_len)
{
    return gnuradio::get_initial_sptr(new fixedlen_tagger_impl(
        sizeof_stream_item, syncword_tag, packetlen_tag, packet_len));
}

/*
 * The private constructor
 */
fixedlen_tagger_impl::fixedlen_tagger_impl(size_t sizeof_stream_item,
                                           const std::string& syncword_tag,
                                           const std::string& packetlen_tag,
                                           size_t packet_len)
    : gr::block("fixedlen_tagger",
                gr::io_signature::make(1, 1, sizeof_stream_item),
                gr::io_signature::make(1, 1, sizeof_stream_item)),
      d_itemsize(sizeof_stream_item),
      d_packet_len(packet_len),
      d_maxtag(-1),
      d_written(0),
      d_really_written(0)
{
    d_syncword_tag = pmt::mp(syncword_tag);
    d_packetlen_tag = pmt::mp(packetlen_tag);
    return;
}

/*
 * Our virtual destructor.
 */
fixedlen_tagger_impl::~fixedlen_tagger_impl() {}

int fixedlen_tagger_impl::try_to_flush(int noutput_items,
                                       gr_vector_void_star& output_items)
{
    size_t len_write =
        std::min(d_data.size(), static_cast<size_t>(noutput_items) * d_itemsize);
    for (size_t j = 0; j < len_write; ++j) {
        ((uint8_t*)output_items[0])[j] = d_data.at(j);
    }
    d_data.erase(d_data.begin(), d_data.begin() + len_write);
    d_really_written += len_write / d_itemsize;

    std::list<uint64_t> tags_to_write_copy = d_tags_to_write;
    for (auto tag_offset : tags_to_write_copy) {
        if (tag_offset < d_really_written) {
            d_tags_to_write.erase(
                std::find(d_tags_to_write.begin(), d_tags_to_write.end(), tag_offset));
            add_item_tag(0, tag_offset, d_packetlen_tag, pmt::from_long(d_packet_len));
        }
    }

    return len_write / d_itemsize;
}

int fixedlen_tagger_impl::general_work(int noutput_items,
                                       gr_vector_int& ninput_items,
                                       gr_vector_const_void_star& input_items,
                                       gr_vector_void_star& output_items)
{
    if (d_data.size()) {
        // write as much as possible without consuming input
        return try_to_flush(noutput_items, output_items);
    }

    d_window.clear();
    d_window.insert(d_window.end(), d_stream.begin(), d_stream.end());
    for (size_t j = 0; j < ninput_items[0] * d_itemsize; ++j) {
        d_window.push_back(((uint8_t*)input_items[0])[j]);
    }

    get_tags_in_range(
        d_alltags, 0, d_maxtag + 1, nitems_read(0) + ninput_items[0], d_syncword_tag);
    for (auto tag : d_alltags) {
        if (std::find(d_tag_offsets.begin(), d_tag_offsets.end(), tag.offset) ==
            d_tag_offsets.end()) {
            // tag not yet seen -> add it
            if (tag.offset > static_cast<uint64_t>(d_maxtag)) {
                d_maxtag = tag.offset;
            }
            d_tag_offsets.push_back(tag.offset);
        }
    }

    std::list<uint64_t> tag_offsets_copy = d_tag_offsets;
    size_t stream_len = d_stream.size() / d_itemsize;
    for (auto tag_offset : tag_offsets_copy) {
        if ((tag_offset >= nitems_read(0) - stream_len) &&
            (static_cast<ssize_t>(tag_offset) <=
             static_cast<ssize_t>(nitems_read(0) + ninput_items[0])
	     - static_cast<ssize_t>(d_packet_len))) {
            d_tag_offsets.erase(
                std::find(d_tag_offsets.begin(), d_tag_offsets.end(), tag_offset));
            auto start = tag_offset - nitems_read(0) + stream_len;
            d_data.insert(d_data.end(),
                          d_window.begin() + start * d_itemsize,
                          d_window.begin() + (start + d_packet_len) * d_itemsize);
            d_tags_to_write.push_back(d_written);
            d_written += d_packet_len;
        }
    }

    for (size_t j = 0; j < ninput_items[0] * d_itemsize; ++j) {
        d_stream.push_back(((uint8_t*)input_items[0])[j]);
    }
    if (d_stream.size() > d_packet_len * d_itemsize) {
        d_stream.erase(d_stream.begin(),
                       d_stream.begin() + d_stream.size() - d_packet_len * d_itemsize);
    }

    consume(0, ninput_items[0]);

    return try_to_flush(noutput_items, output_items);
}


} /* namespace satellites */
} /* namespace gr */
