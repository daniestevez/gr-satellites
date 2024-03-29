/* -*- c++ -*- */
/*
 * Copyright 2017,2020 Daniel Estevez <daniel@destevez.net>
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

#include <gnuradio/logger.h>

#include "nusat_decoder_impl.h"
#include <gnuradio/io_signature.h>

#include "rs.h"

extern "C" {
#include "libfec/fec.h"
}

namespace gr {
namespace satellites {

nusat_decoder::sptr nusat_decoder::make()
{
    return gnuradio::make_block_sptr<nusat_decoder_impl>();
}

const uint8_t nusat_decoder_impl::d_scrambler_sequence[] = {
    0x1D, 0x8B, 0x06, 0x0C, 0x54, 0xDF, 0x21, 0xCB, 0x5C, 0x74, 0xE3, 0x15, 0x68,
    0x04, 0x41, 0x91, 0x7A, 0x3D, 0x7A, 0x81, 0x30, 0x57, 0x1A, 0x0A, 0x09, 0xDB,
    0x33, 0x57, 0x1F, 0x86, 0xEF, 0x58, 0xE0, 0x16, 0xBD, 0x9B, 0xA6, 0x42, 0xFB,
    0x09, 0xD6, 0xCB, 0xE1, 0x27, 0x8E, 0xE7, 0x95, 0x1B, 0x46, 0x4C, 0xEE, 0xC3,
    0x75, 0x7D, 0xA6, 0x1C, 0xF2, 0x45, 0x01, 0x00, 0xFE, 0xAF, 0xFD, 0x03
};

const uint_fast8_t nusat_decoder_impl::crc8_table[256] = {
    0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, 0x38, 0x3f, 0x36, 0x31, 0x24, 0x23,
    0x2a, 0x2d, 0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65, 0x48, 0x4f, 0x46, 0x41,
    0x54, 0x53, 0x5a, 0x5d, 0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5, 0xd8, 0xdf,
    0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd, 0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85,
    0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd, 0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc,
    0xd5, 0xd2, 0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea, 0xb7, 0xb0, 0xb9, 0xbe,
    0xab, 0xac, 0xa5, 0xa2, 0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a, 0x27, 0x20,
    0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32, 0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a,
    0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42, 0x6f, 0x68, 0x61, 0x66, 0x73, 0x74,
    0x7d, 0x7a, 0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c, 0xb1, 0xb6, 0xbf, 0xb8,
    0xad, 0xaa, 0xa3, 0xa4, 0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec, 0xc1, 0xc6,
    0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4, 0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c,
    0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44, 0x19, 0x1e, 0x17, 0x10, 0x05, 0x02,
    0x0b, 0x0c, 0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34, 0x4e, 0x49, 0x40, 0x47,
    0x52, 0x55, 0x5c, 0x5b, 0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63, 0x3e, 0x39,
    0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b, 0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13,
    0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb, 0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d,
    0x84, 0x83, 0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb, 0xe6, 0xe1, 0xe8, 0xef,
    0xfa, 0xfd, 0xf4, 0xf3
};

/*
 * The private constructor
 */
nusat_decoder_impl::nusat_decoder_impl()
    : gr::block("nusat_decoder",
                gr::io_signature::make(0, 0, 0),
                gr::io_signature::make(0, 0, 0))
{
    d_rs = init_rs_char(8, 0x11d, 1, 1, 4, 0);

    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"), [this](pmt::pmt_t msg) { this->msg_handler(msg); });
}

/*
 * Our virtual destructor.
 */
nusat_decoder_impl::~nusat_decoder_impl() { free_rs_char(d_rs); }

void nusat_decoder_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
{
}

int nusat_decoder_impl::general_work(int noutput_items,
                                     gr_vector_int& ninput_items,
                                     gr_vector_const_void_star& input_items,
                                     gr_vector_void_star& output_items)
{
    return 0;
}

uint_fast8_t nusat_decoder_impl::crc8(const uint8_t* data, size_t data_len)
{
    const uint8_t* d = data;
    uint_fast8_t crc = 0;

    while (data_len--)
        crc = crc8_table[crc ^ *d++];
    return crc;
}


void nusat_decoder_impl::msg_handler(pmt::pmt_t pmt_msg)
{
    size_t length(0);
    auto msg = pmt::u8vector_elements(pmt::cdr(pmt_msg), length);

    d_data.fill(0);
    auto msg_length = std::min(length, d_data.size());
    memcpy(d_data.data(), msg, msg_length);

    // Reed-Solomon decoding
    auto rs_res = decode_rs_char(d_rs, d_data.data(), NULL, 0);
    if (rs_res < 0) {
        d_logger->info("Reed-Solomon decoding failed");
        return;
    } else {
        d_logger->info("Reed-Solomon decoding OK");
    }

    length = d_data[d_len_byte];
    if (length >= msg_length - d_header_len) {
        d_logger->info("Length field corrupted");
        return;
    }

    auto packet = &d_data[d_header_len];
    // Descramble
    for (size_t i = 0; i < length; ++i) {
        packet[i] ^= d_scrambler_sequence[i];
    }

    // Compute CRC-8
    if (crc8(packet, length) != d_data[d_crc_byte]) {
        d_logger->info("CRC-8 does not match");
        return;
    }

    // Send by GNUradio message
    message_port_pub(pmt::mp("out"),
                     pmt::cons(pmt::PMT_NIL, pmt::init_u8vector(length, packet)));
}
} /* namespace satellites */
} /* namespace gr */
