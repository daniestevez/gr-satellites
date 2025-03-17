/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "frame_counter_impl.h"
#include <gnuradio/io_signature.h>
#include <pmt/pmt.h>

namespace gr {
namespace satellites {

frame_counter::sptr frame_counter::make(size_t itemsize, size_t frame_size)
{
    return gnuradio::get_initial_sptr(new frame_counter_impl(itemsize, frame_size));
}

frame_counter_impl::frame_counter_impl(size_t itemsize, size_t frame_size)
    : gr::sync_block("frame_counter",
                     gr::io_signature::make(1, 1, itemsize),
                     gr::io_signature::make(1, 1, itemsize)),
      d_itemsize(itemsize),
      d_frame_size(frame_size),
      d_count_port(pmt::string_to_symbol("count"))
{
    message_port_register_out(d_count_port);
}

frame_counter_impl::~frame_counter_impl() {}

int frame_counter_impl::work(int noutput_items,
                             gr_vector_const_void_star& input_items,
                             gr_vector_void_star& output_items)
{
    auto in = static_cast<const uint8_t*>(input_items[0]);
    auto out = static_cast<uint8_t*>(output_items[0]);

    std::memcpy(&out[0], &in[0], noutput_items * d_itemsize);

    d_count += noutput_items;
    const uint64_t n = d_count / d_frame_size;
    if (n != d_last) {
        message_port_pub(d_count_port, pmt::from_uint64(n));
        d_last = n;
    }

    return noutput_items;
}

} /* namespace satellites */
} /* namespace gr */
