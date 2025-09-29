/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "message_counter_impl.h"
#include <gnuradio/io_signature.h>
#include <pmt/pmt.h>

namespace gr {
namespace satellites {

message_counter::sptr message_counter::make()
{
    return gnuradio::make_block_sptr<message_counter_impl>();
}

message_counter_impl::message_counter_impl()
    : gr::sync_block("message_counter",
                     gr::io_signature::make(0, 0, 0),
                     gr::io_signature::make(0, 0, 0)),
      d_out_port(pmt::string_to_symbol("out")),
      d_count_port(pmt::string_to_symbol("count"))
{
    message_port_register_out(d_out_port);
    message_port_register_out(d_count_port);
    const auto in_port = pmt::string_to_symbol("in");
    message_port_register_in(in_port);
    set_msg_handler(in_port, [this](const pmt::pmt_t& msg) { this->msg_handler(msg); });
}

message_counter_impl::~message_counter_impl() {}

int message_counter_impl::work(int noutput_items,
                               gr_vector_const_void_star& input_items,
                               gr_vector_void_star& output_items)
{
    return noutput_items;
}


void message_counter_impl::msg_handler(const pmt::pmt_t& pmt_msg)
{
    message_port_pub(d_out_port, pmt_msg);
    ++d_count;
    message_port_pub(d_count_port, pmt::cons(d_count_port, pmt::from_long(d_count)));
}

} /* namespace satellites */
} /* namespace gr */
