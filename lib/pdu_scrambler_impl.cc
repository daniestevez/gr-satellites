/* -*- c++ -*- */
/*
 * Copyright 2022 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "pdu_scrambler_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
namespace satellites {

pdu_scrambler::sptr pdu_scrambler::make(const std::vector<uint8_t>& sequence)
{
    return gnuradio::make_block_sptr<pdu_scrambler_impl>(sequence);
}

pdu_scrambler_impl::pdu_scrambler_impl(const std::vector<uint8_t>& sequence)
    : gr::block("pdu_scrambler",
                gr::io_signature::make(0, 0, 0),
                gr::io_signature::make(0, 0, 0)),
      d_sequence(sequence)
{
    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"), [this](pmt::pmt_t msg) { this->msg_handler(msg); });
}

pdu_scrambler_impl::~pdu_scrambler_impl() {}

void pdu_scrambler_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
{
}

int pdu_scrambler_impl::general_work(int noutput_items,
                                     gr_vector_int& ninput_items,
                                     gr_vector_const_void_star& input_items,
                                     gr_vector_void_star& output_items)
{
    return 0;
}

void pdu_scrambler_impl::msg_handler(pmt::pmt_t pmt_msg)
{
    std::vector<uint8_t> msg = pmt::u8vector_elements(pmt::cdr(pmt_msg));

    if (msg.size() > d_sequence.size()) {
        d_logger->error("PDU longer than scrambler sequence; dropping");
    }

    for (size_t j = 0; j < msg.size(); ++j) {
        msg[j] ^= d_sequence[j];
    }

    message_port_pub(pmt::mp("out"),
                     pmt::cons(pmt::car(pmt_msg), pmt::init_u8vector(msg.size(), msg)));
}

} /* namespace satellites */
} /* namespace gr */
