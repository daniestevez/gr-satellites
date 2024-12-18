/* -*- c++ -*- */
/*
 * Copyright 2018,2020,2024 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "encode_rs_impl.h"
#include <gnuradio/io_signature.h>

#include <boost/format.hpp>
#include <algorithm>
#include <cstdint>
#include <exception>

extern "C" {
#include "libfec/fec.h"
}

#include "rs.h"

namespace gr {
namespace satellites {

encode_rs::sptr encode_rs::make(bool dual_basis, int interleave)
{
    return gnuradio::get_initial_sptr(new encode_rs_impl(dual_basis, interleave));
}

encode_rs::sptr encode_rs::make(int frame_size, bool dual_basis, int interleave)
{
    return gnuradio::get_initial_sptr(
        new encode_rs_impl(frame_size, dual_basis, interleave));
}

encode_rs::sptr
encode_rs::make(int symsize, int gfpoly, int fcr, int prim, int nroots, int interleave)
{
    return gnuradio::get_initial_sptr(
        new encode_rs_impl(symsize, gfpoly, fcr, prim, nroots, interleave));
}

encode_rs::sptr encode_rs::make(int frame_size,
                                int symsize,
                                int gfpoly,
                                int fcr,
                                int prim,
                                int nroots,
                                int interleave)
{
    return gnuradio::get_initial_sptr(
        new encode_rs_impl(frame_size, symsize, gfpoly, fcr, prim, nroots, interleave));
}

encode_rs_impl::encode_rs_impl(bool dual_basis, int interleave)
    : gr::sync_block(
          "encode_rs", gr::io_signature::make(0, 0, 0), gr::io_signature::make(0, 0, 0)),
      d_interleave(interleave),
      d_frame_size(0)
{
    setup_ccsds(dual_basis);
    set_message_ports();
}

encode_rs_impl::encode_rs_impl(int frame_size, bool dual_basis, int interleave)
    : gr::sync_block("encode_rs",
                     gr::io_signature::make(1, 1, frame_size),
                     gr::io_signature::make(1, 1, d_ccsds_nn * interleave)),
      d_interleave(interleave),
      d_frame_size(frame_size)
{
    check_frame_size();
    setup_ccsds(dual_basis);
}

void encode_rs_impl::setup_ccsds(bool dual_basis)
{
    static constexpr int parity_offset = d_ccsds_nn - d_ccsds_nroots;
    if (dual_basis) {
        d_encode_rs = [](uint8_t* data) {
            encode_rs_ccsds(data, &data[parity_offset], 0);
        };
    } else {
        d_encode_rs = [](uint8_t* data) { encode_rs_8(data, &data[parity_offset], 0); };
    }
    d_rs_codeword.resize(d_ccsds_nn);
    d_nroots = d_ccsds_nroots;

    check_interleave();
}

encode_rs_impl::encode_rs_impl(
    int symsize, int gfpoly, int fcr, int prim, int nroots, int interleave)
    : gr::sync_block(
          "encode_rs", gr::io_signature::make(0, 0, 0), gr::io_signature::make(0, 0, 0)),
      d_interleave(interleave),
      d_frame_size(0)
{
    setup_generic(symsize, gfpoly, fcr, prim, nroots);
    set_message_ports();
}

encode_rs_impl::encode_rs_impl(int frame_size,
                               int symsize,
                               int gfpoly,
                               int fcr,
                               int prim,
                               int nroots,
                               int interleave)
    : gr::sync_block("encode_rs",
                     gr::io_signature::make(1, 1, frame_size),
                     gr::io_signature::make(1, 1, ((1U << symsize) - 1) * interleave)),
      d_interleave(interleave),
      d_frame_size(frame_size)
{
    check_frame_size();
    setup_generic(symsize, gfpoly, fcr, prim, nroots);
}

void encode_rs_impl::setup_generic(int symsize, int gfpoly, int fcr, int prim, int nroots)
{
    d_rs_p = init_rs_char(symsize, gfpoly, fcr, prim, nroots, 0);
    const int codeword_size = (1U << symsize) - 1;
    const int parity_offset = codeword_size - nroots;
    if (!d_rs_p) {
        throw std::runtime_error("Unable to initialize Reed-Solomon definition");
    }
    d_encode_rs = [this, parity_offset](uint8_t* data) {
        return encode_rs_char(d_rs_p, data, &data[parity_offset]);
    };

    d_rs_codeword.resize((1U << symsize) - 1);
    d_nroots = nroots;

    check_interleave();
}

void encode_rs_impl::check_interleave()
{
    if (d_interleave <= 0) {
        throw std::runtime_error(
            boost::str(boost::format("Invalid interleave value = %d") % d_interleave));
    }
}

void encode_rs_impl::check_frame_size()
{
    if (d_frame_size % d_interleave != 0) {
        throw std::runtime_error("Interleave must divide frame size");
    }
}

void encode_rs_impl::set_message_ports()
{
    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"), [this](pmt::pmt_t msg) { this->msg_handler(msg); });
}

encode_rs_impl::~encode_rs_impl()
{
    if (d_rs_p) {
        free_rs_char(d_rs_p);
    }
}

int encode_rs_impl::work(int noutput_items,
                         gr_vector_const_void_star& input_items,
                         gr_vector_void_star& output_items)
{
    auto in = static_cast<const uint8_t*>(input_items[0]);
    auto out = static_cast<uint8_t*>(output_items[0]);

    const auto rs_kk = d_frame_size / d_interleave;
    const auto pad = d_rs_codeword.size() - rs_kk - d_nroots;
    const auto output_frame_size = d_rs_codeword.size() * d_interleave;

    for (int i = 0; i < noutput_items; ++i) {
        for (int j = 0; j < d_interleave; ++j) {
            std::fill(d_rs_codeword.begin(), d_rs_codeword.begin() + pad, 0);
            for (int k = 0; k < rs_kk; ++k) {
                d_rs_codeword[pad + k] = in[j + k * d_interleave];
            }

            d_encode_rs(d_rs_codeword.data());

            for (int k = 0; k < rs_kk + d_nroots; ++k) {
                out[j + k * d_interleave] = d_rs_codeword[pad + k];
            }
        }
        in += d_frame_size;
        out += output_frame_size;
    }

    return noutput_items;
}

void encode_rs_impl::msg_handler(pmt::pmt_t pmt_msg)
{
    auto msg = pmt::u8vector_elements(pmt::cdr(pmt_msg));

    if (msg.size() % d_interleave != 0) {
        GR_LOG_ERROR(
            d_logger,
            boost::format("Reed-Solomon message size not divisible by interleave "
                          "depth. size = %d, interleave = %d") %
                msg.size() % d_interleave);
        return;
    }

    int rs_kk = msg.size() / d_interleave;

    if ((unsigned)(rs_kk + d_nroots) > d_rs_codeword.size()) {
        GR_LOG_ERROR(
            d_logger,
            boost::format("Reed-Solomon message too large. size = %d, interleave "
                          "= %d, RS code (%d, %d)") %
                msg.size() % d_interleave % d_rs_codeword.size() %
                (d_rs_codeword.size() - d_nroots));
        return;
    }

    d_output_frame.resize(msg.size() + d_interleave * d_nroots);
    const auto pad = d_rs_codeword.size() - rs_kk - d_nroots;

    for (int j = 0; j < d_interleave; ++j) {
        std::fill(d_rs_codeword.begin(), d_rs_codeword.begin() + pad, 0);
        for (int k = 0; k < rs_kk; ++k) {
            d_rs_codeword[pad + k] = msg[j + k * d_interleave];
        }

        d_encode_rs(d_rs_codeword.data());

        for (int k = 0; k < rs_kk + d_nroots; ++k) {
            d_output_frame[j + k * d_interleave] = d_rs_codeword[pad + k];
        }
    }

    message_port_pub(
        pmt::mp("out"),
        pmt::cons(pmt::car(pmt_msg),
                  pmt::init_u8vector(d_output_frame.size(), d_output_frame)));
}

} /* namespace satellites */
} /* namespace gr */
