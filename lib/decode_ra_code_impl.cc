/* -*- c++ -*- */
/*
 * Copyright 2019,2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <cstdio>

#include "decode_ra_code_impl.h"
#include <gnuradio/io_signature.h>
#include <gnuradio/logger.h>

extern "C" {
#include "radecoder/ra_decoder_gen.h"
#include "radecoder/ra_encoder.h"
}

namespace gr {
namespace satellites {

decode_ra_code::sptr decode_ra_code::make(int size)
{
    return gnuradio::make_block_sptr<decode_ra_code_impl>(size);
}

/*
 * The private constructor
 */
decode_ra_code_impl::decode_ra_code_impl(int size)
    : gr::block("decode_ra_code",
                gr::io_signature::make(0, 0, 0),
                gr::io_signature::make(0, 0, 0)),
      d_size(size)
{
    d_ra_context = std::unique_ptr<struct ra_context>(new struct ra_context);
    d_ra_out.reserve(d_size);

    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"), [this](pmt::pmt_t msg) { this->msg_handler(msg); });
}

/*
 * Our virtual destructor.
 */
decode_ra_code_impl::~decode_ra_code_impl() {}

void decode_ra_code_impl::forecast(int noutput_items,
                                   gr_vector_int& ninput_items_required)
{
}

int decode_ra_code_impl::general_work(int noutput_items,
                                      gr_vector_int& ninput_items,
                                      gr_vector_const_void_star& input_items,
                                      gr_vector_void_star& output_items)
{
    return 0;
}

void decode_ra_code_impl::msg_handler(pmt::pmt_t pmt_msg)
{
    size_t length(0);
    auto soft_bits = pmt::f32vector_elements(pmt::cdr(pmt_msg), length);

    ra_length_init(d_ra_context.get(), d_size / 2);
    const auto ra_code_length = d_ra_context->ra_code_length;

    if (length != ra_code_length * RA_BITCOUNT) {
        fprintf(stderr,
                "message length: %ld, expected: %d\n",
                (long)length,
                ra_code_length * RA_BITCOUNT);
        GR_LOG_ERROR(d_logger, "Invalid message length");
        return;
    }

    d_ra_in.resize(ra_code_length * RA_BITCOUNT);
    // Weird bit organization: see radecoder/ra_decoder.c
    for (int i = 0; i < ra_code_length * RA_BITCOUNT; i += 8) {
        for (int j = 0; j < 8; j++) {
            d_ra_in[i + j] = -soft_bits[i + 7 - j];
        }
    }

    ra_decoder_gen(d_ra_context.get(), d_ra_in.data(), (ra_word_t*)d_ra_out.data(), 40);

    d_ra_recode.resize(ra_code_length);
    ra_encoder(d_ra_context.get(), (const ra_word_t*)d_ra_out.data(), d_ra_recode.data());

    unsigned errors = 0;
    for (int i = 0; i < ra_code_length; i++) {
        for (int j = 0; j < RA_BITCOUNT; j++) {
            bool bit = (d_ra_recode[i] & (1 << j)) != 0;
            errors += (d_ra_in[i * RA_BITCOUNT + j] >= 0) ? bit : !bit;
        }
    }

    if ((float)errors / (ra_code_length * RA_BITCOUNT) < d_error_threshold) {
        message_port_pub(
            pmt::mp("out"),
            pmt::cons(pmt::PMT_NIL, pmt::init_u8vector(d_size, d_ra_out.data())));
    }
}

} /* namespace satellites */
} /* namespace gr */
