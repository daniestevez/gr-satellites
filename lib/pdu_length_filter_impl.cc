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

#include "pdu_length_filter_impl.h"
#include <gnuradio/io_signature.h>

#include <limits>
#include <vector>

namespace gr {
namespace satellites {

pdu_length_filter::sptr pdu_length_filter::make(int min, int max)
{
    return gnuradio::make_block_sptr<pdu_length_filter_impl>(min, max);
}

/*
 * The private constructor
 */
pdu_length_filter_impl::pdu_length_filter_impl(int min, int max)
    : gr::block("pdu_length_filter",
                gr::io_signature::make(0, 0, 0),
                gr::io_signature::make(0, 0, 0)),
      d_min(min)
{
    // max < 0 means unlimited length
    d_max =
        max < 0 ? (size_t)std::numeric_limits<size_t>::max() : static_cast<size_t>(max);
    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"), [this](pmt::pmt_t msg) { this->msg_handler(msg); });
}

/*
 * Our virtual destructor.
 */
pdu_length_filter_impl::~pdu_length_filter_impl() {}

void pdu_length_filter_impl::forecast(int noutput_items,
                                      gr_vector_int& ninput_items_required)
{
}

int pdu_length_filter_impl::general_work(int noutput_items,
                                         gr_vector_int& ninput_items,
                                         gr_vector_const_void_star& input_items,
                                         gr_vector_void_star& output_items)
{
    return 0;
}

void pdu_length_filter_impl::msg_handler(pmt::pmt_t pmt_msg)
{
    std::vector<uint8_t> msg = pmt::u8vector_elements(pmt::cdr(pmt_msg));

    if ((msg.size() >= d_min) && (msg.size() <= d_max)) {
        message_port_pub(pmt::mp("out"), pmt_msg);
    }
}

} /* namespace satellites */
} /* namespace gr */
