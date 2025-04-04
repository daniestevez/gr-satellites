/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>
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
#include <cstdio>
#include <stdexcept>

#include "u482c_encode_impl.h"
#include <gnuradio/io_signature.h>

extern "C" {
#include "golay24.h"
#include "libfec/fec.h"
#include "randomizer.h"
}

namespace gr {
namespace satellites {

u482c_encode::sptr u482c_encode::make(
    bool convolutional, bool scrambler, bool rs, int preamble_len, bool flags_in_golay)
{
    return gnuradio::get_initial_sptr(new u482c_encode_impl(
        convolutional, scrambler, rs, preamble_len, flags_in_golay));
}

u482c_encode_impl::u482c_encode_impl(
    bool convolutional, bool scrambler, bool rs, int preamble_len, bool flags_in_golay)
    : gr::sync_block("u482c_encode",
                     gr::io_signature::make(0, 0, 0),
                     gr::io_signature::make(0, 0, 0)),
      d_convolutional(convolutional),
      d_scrambler(scrambler),
      d_rs(rs),
      d_preamble_len(preamble_len),
      d_flags_in_golay(flags_in_golay)
{
    if (convolutional) {
        throw std::runtime_error("[u482c_encode] convolutional coding not supported yet");
    }

    if (d_scrambler) {
        ccsds_generate_sequence(d_ccsds_sequence.data(), d_ccsds_sequence.size());
    }

    // Fill d_data with 0xAA bytes. The first d_preamble_len of these will never
    // be overwitten and always used as preamble.
    d_data.resize(d_preamble_len + k_syncword_len + k_header_len + k_rs_coded_len, 0xAA);
    // Fill syncword. This will never be overwitten.
    std::copy(k_syncword.cbegin(), k_syncword.cend(), d_data.begin() + d_preamble_len);

    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"),
                    [this](const pmt::pmt_t& msg) { this->msg_handler(msg); });
}

u482c_encode_impl::~u482c_encode_impl() {}

int u482c_encode_impl::work(int noutput_items,
                            gr_vector_const_void_star& input_items,
                            gr_vector_void_star& output_items)
{
    return noutput_items;
}

void u482c_encode_impl::msg_handler(const pmt::pmt_t& pmt_msg)
{
    auto msg = pmt::u8vector_elements(pmt::cdr(pmt_msg));
    const auto max_payload_len = d_rs ? k_rs_info_len : k_rs_coded_len;
    auto payload_len = msg.size();
    if (payload_len > max_payload_len) {
        printf("payload length %d is too long; dropping message",
               static_cast<int>(payload_len));
        return;
    }

    // Header
    //
    // In RS mode, the header frame_len field contains the length of the encoded
    // payload.
    const uint8_t frame_len =
        d_rs ? payload_len + k_rs_coded_len - k_rs_info_len : payload_len;
    uint32_t header = frame_len;
    if (d_flags_in_golay) {
        header |= (d_convolutional << 8) | (d_scrambler << 9) | (d_rs << 10);
    }
    encode_golay24(&header);
    const auto p_header = &d_data[d_preamble_len + k_syncword_len];
    p_header[0] = (header >> 16) & 0xff;
    p_header[1] = (header >> 8) & 0xff;
    p_header[2] = header & 0xff;

    // copy payload to buffer
    const auto payload = &p_header[k_header_len];
    std::copy(msg.cbegin(), msg.cend(), payload);

    // Reed-Solomon encoding
    if (d_rs) {
        encode_rs_8(payload, payload + payload_len, k_rs_info_len - payload_len);
        payload_len += k_rs_coded_len - k_rs_info_len;
    }

    // CCSDS scrambling
    if (d_scrambler) {
        ccsds_xor_sequence(payload, &d_ccsds_sequence[0], payload_len);
    }

    // Send via GNU Radio message
    message_port_pub(
        pmt::mp("out"),
        pmt::cons(
            pmt::PMT_NIL,
            pmt::init_u8vector(d_preamble_len + k_header_len + payload_len, &d_data[0])));
}
} /* namespace satellites */
} /* namespace gr */
