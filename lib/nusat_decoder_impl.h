/* -*- c++ -*- */
/*
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_NUSAT_DECODER_IMPL_H
#define INCLUDED_SATELLITES_NUSAT_DECODER_IMPL_H

#include <pmt/pmt.h>
#include <satellites/nusat_decoder.h>

#include <stdint.h>

#include <array>

#include "rs.h"

namespace gr {
namespace satellites {

class nusat_decoder_impl : public nusat_decoder
{
private:
    constexpr static size_t d_msg_len = 64;
    constexpr static size_t d_header_len = 2;
    constexpr static size_t d_len_byte = 0;
    constexpr static size_t d_crc_byte = 1;
    static const uint8_t d_scrambler_sequence[];
    static const uint_fast8_t crc8_table[];
    void* d_rs;
    std::array<uint8_t, MAX_FRAME_LEN> d_data;

    uint_fast8_t crc8(const uint8_t* data, size_t data_len);

public:
    nusat_decoder_impl();
    ~nusat_decoder_impl();

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

#endif /* INCLUDED_SATELLITES_NUSAT_DECODER_IMPL_H */
