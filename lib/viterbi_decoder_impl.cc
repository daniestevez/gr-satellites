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

#include "viterbi_decoder_impl.h"
#include <gnuradio/io_signature.h>

#include <string>
#include <vector>

namespace gr {
namespace satellites {

viterbi_decoder::sptr viterbi_decoder::make(int constraint,
                                            const std::vector<int>& polynomials)
{
    return gnuradio::make_block_sptr<viterbi_decoder_impl>(constraint, polynomials);
}

/*
 * The private constructor
 */
viterbi_decoder_impl::viterbi_decoder_impl(int constraint,
                                           const std::vector<int>& polynomials)
    : gr::block("viterbi_decoder",
                gr::io_signature::make(0, 0, 0),
                gr::io_signature::make(0, 0, 0)),
      d_codec(constraint, polynomials)
{
    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"), [this](pmt::pmt_t msg) { this->msg_handler(msg); });
}

/*
 * Our virtual destructor.
 */
viterbi_decoder_impl::~viterbi_decoder_impl() {}

int viterbi_decoder_impl::general_work(int noutput_items,
                                       gr_vector_int& ninput_items,
                                       gr_vector_const_void_star& input_items,
                                       gr_vector_void_star& output_items)
{
    return 0;
}


void viterbi_decoder_impl::msg_handler(pmt::pmt_t pmt_msg)
{
    std::vector<uint8_t> msg = pmt::u8vector_elements(pmt::cdr(pmt_msg));
    std::string bits;
    for (auto b : msg) {
        bits.push_back(b ? '1' : '0');
    }

    std::string outbits = d_codec.Decode(bits);
    std::vector<uint8_t> out;
    for (auto b : outbits) {
        out.push_back(b == '1');
    }

    message_port_pub(pmt::mp("out"),
                     pmt::cons(pmt::car(pmt_msg), pmt::init_u8vector(out.size(), out)));

    return;
}


} /* namespace satellites */
} /* namespace gr */
