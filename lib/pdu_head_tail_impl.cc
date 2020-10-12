/* -*- c++ -*- */
/*
 * Copyright 2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "pdu_head_tail_impl.h"
#include <gnuradio/io_signature.h>

#include <algorithm>
#include <vector>

namespace gr {
namespace satellites {

pdu_head_tail::sptr pdu_head_tail::make(int mode, size_t num)
{
    return gnuradio::get_initial_sptr(new pdu_head_tail_impl(mode, num));
}

/*
 * The private constructor
 */
pdu_head_tail_impl::pdu_head_tail_impl(int mode, size_t num)
    : gr::block("pdu_head_tail",
                gr::io_signature::make(0, 0, 0),
                gr::io_signature::make(0, 0, 0)),
      d_mode(mode),
      d_num(num)
{
    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"),
                    boost::bind(&pdu_head_tail_impl::msg_handler, this, _1));
}

/*
 * Our virtual destructor.
 */
pdu_head_tail_impl::~pdu_head_tail_impl() {}

void pdu_head_tail_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
{
}

int pdu_head_tail_impl::general_work(int noutput_items,
                                     gr_vector_int& ninput_items,
                                     gr_vector_const_void_star& input_items,
                                     gr_vector_void_star& output_items)
{
    return 0;
}

void pdu_head_tail_impl::msg_handler(pmt::pmt_t pmt_msg)
{
    std::vector<uint8_t> msg = pmt::u8vector_elements(pmt::cdr(pmt_msg));
    std::vector<uint8_t> cut_msg;
    auto num = std::min(d_num, msg.size());

    switch (d_mode) {
    case PDU_HEADTAIL_HEAD:
        cut_msg = std::vector<uint8_t>(msg.begin(), msg.begin() + num);
        break;
    case PDU_HEADTAIL_HEADMINUS:
        cut_msg = std::vector<uint8_t>(msg.begin(), msg.end() - num);
        break;
    case PDU_HEADTAIL_TAIL:
        cut_msg = std::vector<uint8_t>(msg.end() - num, msg.end());
        break;
    case PDU_HEADTAIL_TAILPLUS:
        cut_msg = std::vector<uint8_t>(msg.begin() + num, msg.end());
        break;
    default:
        throw "Invalid pdu_head_tail mode";
        break;
    }

    message_port_pub(
        pmt::mp("out"),
        pmt::cons(pmt::car(pmt_msg), pmt::init_u8vector(cut_msg.size(), cut_msg)));
}

} /* namespace satellites */
} /* namespace gr */
