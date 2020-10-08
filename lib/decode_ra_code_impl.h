/* -*- c++ -*- */
/*
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_DECODE_RA_CODE_IMPL_H
#define INCLUDED_SATELLITES_DECODE_RA_CODE_IMPL_H

#include <satellites/decode_ra_code.h>

#include <memory>
#include <vector>

extern "C" {
#include "radecoder/ra_config.h"
}

namespace gr {
namespace satellites {

class decode_ra_code_impl : public decode_ra_code
{
private:
    constexpr static float d_error_threshold = 0.35f;
    int d_size;
    std::unique_ptr<struct ra_context> d_ra_context;
    std::vector<float> d_ra_in;
    std::vector<uint8_t> d_ra_out;
    std::vector<ra_word_t> d_ra_recode;

public:
    decode_ra_code_impl(int size);
    ~decode_ra_code_impl();

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

#endif /* INCLUDED_SATELLITES_DECODE_RA_CODE_IMPL_H */
