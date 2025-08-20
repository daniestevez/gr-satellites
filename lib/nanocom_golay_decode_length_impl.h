/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_NANOCOM_GOLAY_DECODE_LENGTH_IMPL_H
#define INCLUDED_SATELLITES_NANOCOM_GOLAY_DECODE_LENGTH_IMPL_H

#include <pmt/pmt.h>
#include <satellites/nanocom_golay_decode_length.h>

namespace gr {
namespace satellites {

class nanocom_golay_decode_length_impl : public nanocom_golay_decode_length
{
private:
    const pmt::pmt_t d_golay_start_tag_key;
    const pmt::pmt_t d_length_tag_key;
    const int k_golay_N = 24;

public:
    nanocom_golay_decode_length_impl(const std::string& golay_start_tag_key,
                                     const std::string& length_tag_key);
    ~nanocom_golay_decode_length_impl() override;

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items) override;
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_NANOCOM_GOLAY_DECODE_LENGTH_IMPL_H */
