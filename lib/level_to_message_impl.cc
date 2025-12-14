/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "level_to_message_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
namespace satellites {

level_to_message::sptr level_to_message::make(float threshold)
{
    return gnuradio::make_block_sptr<level_to_message_impl>(threshold);
}

level_to_message_impl::level_to_message_impl(float threshold)
    : gr::sync_block("level_to_message",
                     gr::io_signature::make(1, 1, sizeof(float)),
                     gr::io_signature::make(0, 0, 0)),
      d_threshold(threshold),
      d_out_port(pmt::string_to_symbol("out")),
      d_above_tag(pmt::string_to_symbol("above_threshold"))
{
    message_port_register_out(d_out_port);
}

level_to_message_impl::~level_to_message_impl() {}

int level_to_message_impl::work(int noutput_items,
                                gr_vector_const_void_star& input_items,
                                gr_vector_void_star& output_items)
{
    auto in = static_cast<const float*>(input_items[0]);

    const bool above_threshold = in[noutput_items - 1] > d_threshold;
    if (above_threshold != d_above_threshold) {
        d_above_threshold = above_threshold;
        message_port_pub(d_out_port,
                         pmt::cons(d_above_tag, pmt::from_bool(above_threshold)));
    }

    return noutput_items;
}

} /* namespace satellites */
} /* namespace gr */
