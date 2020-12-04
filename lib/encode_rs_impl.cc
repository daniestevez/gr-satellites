/* -*- c++ -*- */
/*
 * Copyright 2018,2020 Daniel Estevez <daniel@destevez.net>
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

encode_rs::sptr
encode_rs::make(int symsize, int gfpoly, int fcr, int prim, int nroots, int interleave)
{
    return gnuradio::get_initial_sptr(
        new encode_rs_impl(symsize, gfpoly, fcr, prim, nroots, interleave));
}

/*
 * The private constructor
 */
encode_rs_impl::encode_rs_impl(bool dual_basis, int interleave)
    : gr::block(
          "encode_rs", gr::io_signature::make(0, 0, 0), gr::io_signature::make(0, 0, 0)),
      d_interleave(interleave)
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
    set_message_ports();
}

/*
 * The private constructor
 */
encode_rs_impl::encode_rs_impl(
    int symsize, int gfpoly, int fcr, int prim, int nroots, int interleave)
    : gr::block(
          "encode_rs", gr::io_signature::make(0, 0, 0), gr::io_signature::make(0, 0, 0)),
      d_interleave(interleave)
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
    set_message_ports();
}

void encode_rs_impl::check_interleave()
{
    if (d_interleave <= 0) {
        throw std::runtime_error(
            boost::str(boost::format("Invalid interleave value = %d") % d_interleave));
    }
}

void encode_rs_impl::set_message_ports()
{
    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"), [this](pmt::pmt_t msg) { this->msg_handler(msg); });
}

/*
 * Our virtual destructor.
 */
encode_rs_impl::~encode_rs_impl()
{
    if (d_rs_p) {
        free_rs_char(d_rs_p);
    }
}

void encode_rs_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required) {}

int encode_rs_impl::general_work(int noutput_items,
                                 gr_vector_int& ninput_items,
                                 gr_vector_const_void_star& input_items,
                                 gr_vector_void_star& output_items)
{
    return 0;
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
