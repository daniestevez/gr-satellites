/* -*- c++ -*- */
/*
 * Copyright 2016 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_U482C_DECODE_IMPL_H
#define INCLUDED_SATELLITES_U482C_DECODE_IMPL_H

#include <pmt/pmt.h>
#include <satellites/u482c_decode.h>

#include <array>

namespace gr {
namespace satellites {

class u482c_decode_impl : public u482c_decode
{
private:
    constexpr static size_t d_rs_len = 255;
    constexpr static size_t d_header_len = 3;
    const bool d_verbose;
    std::array<char, d_rs_len> d_ccsds_sequence;
    std::array<uint8_t, d_header_len + d_rs_len> d_data;
    std::array<uint8_t, d_rs_len> d_rs_scratch;
    void* d_vp;
    const int d_viterbi;
    const int d_scrambler;
    const int d_rs;

public:
    u482c_decode_impl(bool verbose, int viterbi, int scrambler, int rs);
    ~u482c_decode_impl();

    // Where all the action really happens
    void forecast(int noutput_items, gr_vector_int& ninput_items_required);

    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items);

    void msg_handler(pmt::pmt_t pmt_msg);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_U482C_DECODE_IMPL_H */
