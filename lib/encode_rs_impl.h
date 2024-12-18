/* -*- c++ -*- */
/*
 * Copyright 2018,2020, 2024 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_ENCODE_RS_IMPL_H
#define INCLUDED_SATELLITES_ENCODE_RS_IMPL_H

#include <satellites/encode_rs.h>

#include <cstdint>
#include <functional>
#include <vector>

namespace gr {
namespace satellites {

class encode_rs_impl : public encode_rs
{
private:
    int d_interleave;
    std::vector<uint8_t> d_rs_codeword;
    std::vector<uint8_t> d_output_frame;
    int d_nroots;
    void* d_rs_p = NULL;
    const int d_frame_size; // used only with vector stream IO

    std::function<void(uint8_t*)> d_encode_rs;

    constexpr static int d_ccsds_nn = 255;
    constexpr static int d_ccsds_nroots = 32;

    void setup_ccsds(bool dual_basis);
    void setup_generic(int symsize, int gfpoly, int fcr, int prim, int nroots);
    void check_interleave();
    void check_frame_size();
    void set_message_ports();

public:
    encode_rs_impl(bool dual_basis, int interleave = 1);
    encode_rs_impl(int frame_size, bool dual_basis, int interleave = 1);
    encode_rs_impl(
        int symsize, int gfpoly, int fcr, int prim, int nroots, int interleave = 1);
    encode_rs_impl(int frame_size,
                   int symsize,
                   int gfpoly,
                   int fcr,
                   int prim,
                   int nroots,
                   int interleave);
    ~encode_rs_impl() override;

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items) override;

    void msg_handler(pmt::pmt_t pmt_msg);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_ENCODE_RS_IMPL_H */
