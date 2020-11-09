/* -*- c++ -*- */
/*
 * Copyright 2018,2020 Daniel Estevez <daniel@destevez.net>
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

    std::function<void(uint8_t*)> d_encode_rs;

    constexpr static int d_ccsds_nn = 255;
    constexpr static int d_ccsds_nroots = 32;

    void check_interleave();
    void set_message_ports();

public:
    encode_rs_impl(bool dual_basis, int interleave = 1);
    encode_rs_impl(
        int symsize, int gfpoly, int fcr, int prim, int nroots, int interleave = 1);
    ~encode_rs_impl();

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

#endif /* INCLUDED_SATELLITES_ENCODE_RS_IMPL_H */
