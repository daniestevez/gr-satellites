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

#include <boost/format.hpp>
#include <algorithm>
#include <exception>

extern "C" {
#include "libfec/fec.h"
}

namespace gr {
namespace satellites {

decode_rs::sptr decode_rs::make(int dual_basis, int interleave)
{
    return gnuradio::make_block_sptr<decode_rs_impl>(dual_basis, interleave);
}

decode_rs::sptr
decode_rs::make(int symsize, int gfpoly, int fcr, int prim, int nroots, int interleave)
{
    return gnuradio::make_block_sptr<decode_rs_impl>(
        symsize, gfpoly, fcr, prim, nroots, interleave);
}

/*
 * The private constructor
 */
decode_rs_impl::decode_rs_impl(bool dual_basis, int interleave)
    : gr::block(
          "decode_rs", gr::io_signature::make(0, 0, 0), gr::io_signature::make(0, 0, 0)),
      d_interleave(interleave)
{
    if (dual_basis) {
        d_decode_rs = [](uint8_t* data) { return decode_rs_ccsds(data, NULL, 0, 0); };
    } else {
        d_decode_rs = [](uint8_t* data) { return decode_rs_8(data, NULL, 0, 0); };
    }
    d_rs_codeword.resize(d_ccsds_nn);
    d_nroots = d_ccsds_nroots;

    check_interleave();
    set_message_ports();
}

/*
 * The private constructor
 */
decode_rs_impl::decode_rs_impl(
    int symsize, int gfpoly, int fcr, int prim, int nroots, int interleave)
    : gr::block(
          "decode_rs", gr::io_signature::make(0, 0, 0), gr::io_signature::make(0, 0, 0)),
      d_interleave(interleave)
{
    d_rs_p = init_rs_char(symsize, gfpoly, fcr, prim, nroots, 0);
    if (!d_rs_p) {
        throw std::runtime_error("Unable to initialize Reed-Solomon definition");
    }
    d_decode_rs = [this](uint8_t* data) { return decode_rs_char(d_rs_p, data, 0, 0); };

    d_rs_codeword.resize((1U << symsize) - 1);
    d_nroots = nroots;

    check_interleave();
    set_message_ports();
}

void decode_rs_impl::check_interleave()
{
    if (d_interleave <= 0) {
        throw std::runtime_error(
            boost::str(boost::format("Invalid interleave value = %d") % d_interleave));
    }
}

void decode_rs_impl::set_message_ports()
{
    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"), [this](pmt::pmt_t msg) { this->msg_handler(msg); });
}

/*
 * Our virtual destructor.
 */
decode_rs_impl::~decode_rs_impl()
{
    if (d_rs_p) {
        free_rs_char(d_rs_p);
    }
}

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
    auto msg = pmt::u8vector_elements(pmt::cdr(pmt_msg));
    int errors = 0;

    if (msg.size() % d_interleave != 0) {
        GR_LOG_WARN(d_logger,
                    boost::format("Reed-Solomon message size not divisible by interleave "
                                  "depth. size = %d, interleave = %d") %
                        msg.size() % d_interleave);
        return;
    }

    int rs_nn = msg.size() / d_interleave;
    if (rs_nn <= d_nroots || (unsigned)rs_nn > d_rs_codeword.size()) {
        GR_LOG_ERROR(
            d_logger,
            boost::format("Wrong Reed-Solomon message size. size = %d, interleave "
                          "= %d, RS code (%d, %d)") %
                msg.size() % d_interleave % d_rs_codeword.size() %
                (d_rs_codeword.size() - d_nroots));
        return;
    }

    d_output_frame.resize(msg.size() - d_interleave * d_nroots);
    const auto pad = d_rs_codeword.size() - rs_nn;

    for (int j = 0; j < d_interleave; ++j) {
        std::fill(d_rs_codeword.begin(), d_rs_codeword.begin() + pad, 0);
        for (int k = 0; k < rs_nn; ++k) {
            d_rs_codeword[pad + k] = msg[j + k * d_interleave];
        }

        auto rs_res = d_decode_rs(d_rs_codeword.data());
        if (rs_res < 0) {
            GR_LOG_DEBUG(d_logger,
                         boost::format("Reed-Solomon decode fail (interleaver path %d)") %
                             j);
            return;
        }
        GR_LOG_DEBUG(d_logger,
                     boost::format(
                         "Reed-Solomon decode corrected %d bytes (interleaver path %d)") %
                         rs_res % j);
        errors += rs_res;

        for (int k = 0; k < rs_nn - d_nroots; ++k) {
            d_output_frame[j + k * d_interleave] = d_rs_codeword[pad + k];
        }
    }

    auto meta =
        pmt::dict_add(pmt::car(pmt_msg), pmt::mp("rs_errors"), pmt::from_long(errors));

    message_port_pub(
        pmt::mp("out"),
        pmt::cons(meta, pmt::init_u8vector(d_output_frame.size(), d_output_frame)));
}

} /* namespace satellites */
} /* namespace gr */
