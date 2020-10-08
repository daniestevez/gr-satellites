/* -*- c++ -*- */
/*
 * Copyright 2019-2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "decode_rs_interleaved_impl.h"
#include <gnuradio/io_signature.h>

#include <cstdio>

extern "C" {
#include "libfec/fec.h"
}

#include "rs.h"

namespace gr {
namespace satellites {

decode_rs_interleaved::sptr
decode_rs_interleaved::make(bool verbose, int basis, int codewords)
{
    return gnuradio::get_initial_sptr(
        new decode_rs_interleaved_impl(verbose, basis, codewords));
}

/*
 * The private constructor
 */
decode_rs_interleaved_impl::decode_rs_interleaved_impl(bool verbose,
                                                       int basis,
                                                       int codewords)
    : gr::block(
          "decode_rs", gr::io_signature::make(0, 0, 0), gr::io_signature::make(0, 0, 0)),
      d_verbose(verbose),
      d_basis(basis),
      d_codewords(codewords)
{
    d_out.resize((MAX_FRAME_LEN - 32) * d_codewords);

    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"),
                    boost::bind(&decode_rs_interleaved_impl::msg_handler, this, _1));
}

/*
 * Our virtual destructor.
 */
decode_rs_interleaved_impl::~decode_rs_interleaved_impl() {}

void decode_rs_interleaved_impl::forecast(int noutput_items,
                                          gr_vector_int& ninput_items_required)
{
}

int decode_rs_interleaved_impl::general_work(int noutput_items,
                                             gr_vector_int& ninput_items,
                                             gr_vector_const_void_star& input_items,
                                             gr_vector_void_star& output_items)
{
    return 0;
}

void decode_rs_interleaved_impl::msg_handler(pmt::pmt_t pmt_msg)
{
    size_t length(0);
    auto data = pmt::u8vector_elements(pmt::cdr(pmt_msg), length);
    int rs_res;
    int total_errors = 0;

    if (length != MAX_FRAME_LEN * d_codewords) {
        if (d_verbose) {
            std::printf("Reed-Solomon decoder: invalid frame length %ld\n", (long)length);
        }
        return;
    }

    for (size_t j = 0; j < d_codewords; ++j) {
        for (size_t k = 0; k < d_codeword.size(); ++k) {
            d_codeword[k] = data[j + d_codewords * k];
        }

        if (d_basis == BASIS_CONVENTIONAL) {
            rs_res = decode_rs_8(d_codeword.data(), NULL, 0, 0);
        } else {
            rs_res = decode_rs_ccsds(d_codeword.data(), NULL, 0, 0);
        }

        if (rs_res < 0) {
            if (d_verbose) {
                std::printf("Reed-Solomon decode failed.\n");
            }
            return;
        }

        total_errors += rs_res;

        for (size_t k = 0; k < d_codeword.size() - PARITY_BYTES; ++k) {
            d_out[j + d_codewords * k] = d_codeword[k];
        }
    }

    if (d_verbose) {
        std::printf("Reed-Solomon decode OK. Bytes corrected: %d.\n", total_errors);
    }

    // Send by GNUradio message
    message_port_pub(
        pmt::mp("out"),
        pmt::cons(pmt::PMT_NIL, pmt::init_u8vector(d_out.size(), d_out.data())));
}

} /* namespace satellites */
} /* namespace gr */
