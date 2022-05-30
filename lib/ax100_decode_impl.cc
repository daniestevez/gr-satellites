/* -*- c++ -*- */
/*
 * Copyright 2016,2020 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <algorithm>
#include <utility>

#include <cstdio>
#include <cstring>

#include "ax100_decode_impl.h"
#include <gnuradio/io_signature.h>

extern "C" {
#include "libfec/fec.h"
}

namespace gr {
namespace satellites {

ax100_decode::sptr ax100_decode::make(bool verbose)
{
    return gnuradio::make_block_sptr<ax100_decode_impl>(verbose);
}

/*
 * The private constructor
 */
ax100_decode_impl::ax100_decode_impl(bool verbose)
    : gr::block("ax100_decode",
                gr::io_signature::make(0, 0, 0),
                gr::io_signature::make(0, 0, 0)),
      d_verbose(verbose)
{
    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"), [this](pmt::pmt_t msg) { this->msg_handler(msg); });
}

/*
 * Our virtual destructor.
 */
ax100_decode_impl::~ax100_decode_impl() {}

void ax100_decode_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
{
}

int ax100_decode_impl::general_work(int noutput_items,
                                    gr_vector_int& ninput_items,
                                    gr_vector_const_void_star& input_items,
                                    gr_vector_void_star& output_items)
{
    return 0;
}

void ax100_decode_impl::msg_handler(pmt::pmt_t pmt_msg)
{
    size_t length(0);
    auto msg = pmt::u8vector_elements(pmt::cdr(pmt_msg), length);

    length = std::min(length, d_data.size());
    std::memcpy(d_data.data(), msg, length);

    auto rs_res = decode_rs_8(&d_data[1], NULL, 0, 255 - d_data[0] + 1);

    // Send via GNUradio message if RS ok
    if (rs_res >= 0) {
        // 32 RS parity symbols, 1 includes the length byte
        auto frame_len = d_data[0] - 32 - 1;
        if (frame_len < 0) {
            return;
        }

        if (d_verbose) {
            std::printf(
                "RS decode OK. Length: %d. Bytes corrected: %d.\n", frame_len, rs_res);
        }

        // Send by GNUradio message
        message_port_pub(
            pmt::mp("out"),
            pmt::cons(pmt::PMT_NIL, pmt::init_u8vector(frame_len, &d_data[1])));
    } else if (d_verbose) {
        std::printf("RS decode failed.\n");
    }
}

} /* namespace satellites */
} /* namespace gr */
