/* -*- c++ -*- */
/*
 * Copyright 2021 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_FIXEDLEN_TAGGER_IMPL_H
#define INCLUDED_SATELLITES_FIXEDLEN_TAGGER_IMPL_H

#include <satellites/fixedlen_tagger.h>

#include <deque>
#include <list>

namespace gr {
namespace satellites {

class fixedlen_tagger_impl : public fixedlen_tagger
{
private:
    size_t d_itemsize;
    pmt::pmt_t d_syncword_tag;
    pmt::pmt_t d_packetlen_tag;
    size_t d_packet_len;
    ssize_t d_maxtag;
    std::list<uint64_t> d_tag_offsets;
    std::list<uint64_t> d_tag_offsets_copy;
    std::vector<tag_t> d_alltags;
    std::deque<uint8_t> d_stream;
    std::deque<uint8_t> d_data;
    std::vector<uint8_t> d_window;
    uint64_t d_written;
    uint64_t d_really_written;
    std::list<uint64_t> d_tags_to_write;
    std::list<uint64_t> d_tags_to_write_copy;

    int try_to_flush(int noutput_items, gr_vector_void_star& output_items);

public:
    fixedlen_tagger_impl(size_t sizeof_stream_item,
                         const std::string& syncword_tag,
                         const std::string& packetlen_tag,
                         size_t packet_len);
    ~fixedlen_tagger_impl();

    // Where all the action really happens
    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_FIXEDLEN_TAGGER_IMPL_H */
