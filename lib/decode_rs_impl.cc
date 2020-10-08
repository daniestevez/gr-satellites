/* -*- c++ -*- */
/*
 * Copyright 2016,2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "decode_rs_impl.h"
#include <gnuradio/io_signature.h>

#include <cstdio>

extern "C" {
#include "libfec/fec.h"
}

#include "rs.h"

namespace gr {
namespace satellites {

decode_rs::sptr decode_rs::make(bool verbose, int basis)
{
    return gnuradio::get_initial_sptr(new decode_rs_impl(verbose, basis));
}

/*
 * The private constructor
 */
decode_rs_impl::decode_rs_impl(bool verbose, int basis)
    : gr::block(
          "decode_rs", gr::io_signature::make(0, 0, 0), gr::io_signature::make(0, 0, 0)),
      d_verbose(verbose),
      d_basis(basis)
{
    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"), boost::bind(&decode_rs_impl::msg_handler, this, _1));
}

/*
 * Our virtual destructor.
 */
decode_rs_impl::~decode_rs_impl() {}

void decode_rs_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required) {}

int decode_rs_impl::general_work(int noutput_items,
                                 gr_vector_int& ninput_items,
                                 gr_vector_const_void_star& input_items,
                                 gr_vector_void_star& output_items)
{
    return 0;
}

void decode_rs_impl::msg_handler(pmt::pmt_t pmt_msg)
{
    size_t length(0);
    auto msg = pmt::u8vector_elements(pmt::cdr(pmt_msg), length);
    int rs_res;

    if (length <= PARITY_BYTES || length > d_data.size()) {
        if (d_verbose) {
            std::printf("Reed-Solomon decoder: invalid frame length %ld\n", (long)length);
        }
        return;
    }

    memcpy(d_data.data(), msg, length);

    if (d_basis == BASIS_CONVENTIONAL) {
        rs_res = decode_rs_8(d_data.data(), NULL, 0, MAX_FRAME_LEN - length);
    } else {
        rs_res = decode_rs_ccsds(d_data.data(), NULL, 0, MAX_FRAME_LEN - length);
    }

    // Send via GNUradio message if RS ok
    if (rs_res >= 0) {
        length -= PARITY_BYTES;

        if (d_verbose) {
            std::printf("Reed-Solomon decode OK. Bytes corrected: %d.\n", rs_res);
        }

        // Send by GNUradio message
        message_port_pub(
            pmt::mp("out"),
            pmt::cons(pmt::PMT_NIL, pmt::init_u8vector(length, d_data.data())));
    } else if (d_verbose) {
        std::printf("Reed-Solomon decode failed.\n");
    }
}

} /* namespace satellites */
} /* namespace gr */
