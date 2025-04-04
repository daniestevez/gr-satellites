/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_U482C_ENCODE_IMPL_H
#define INCLUDED_SATELLITES_U482C_ENCODE_IMPL_H

#include <pmt/pmt.h>
#include <satellites/u482c_encode.h>
#include <array>
#include <vector>

namespace gr {
namespace satellites {

class u482c_encode_impl : public u482c_encode
{
private:
    static constexpr size_t k_rs_coded_len = 255;
    static constexpr size_t k_rs_info_len = 223;
    static constexpr size_t k_header_len = 3;
    static constexpr size_t k_syncword_len = 4;
    static constexpr std::array<uint8_t, k_syncword_len> k_syncword{
        0x93, 0x0b, 0x51, 0xde
    };
    std::array<char, k_rs_coded_len> d_ccsds_sequence;
    std::vector<uint8_t> d_data;
    const bool d_convolutional;
    const bool d_scrambler;
    const bool d_rs;
    const int d_preamble_len;
    const bool d_flags_in_golay;

public:
    u482c_encode_impl(bool convolutional,
                      bool scrambler,
                      bool rs,
                      int preamble_len,
                      bool flags_in_golay);
    ~u482c_encode_impl() override;

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items) override;

    void msg_handler(const pmt::pmt_t& pmt_msg);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_U482C_ENCODE_IMPL_H */
