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

#include "matrix_deinterleaver_soft_impl.h"
#include <gnuradio/io_signature.h>

#include <stdexcept>

namespace gr {
namespace satellites {

matrix_deinterleaver_soft::sptr
matrix_deinterleaver_soft::make(int rows, int cols, int output_size, int output_skip)
{
    return gnuradio::get_initial_sptr(
        new matrix_deinterleaver_soft_impl(rows, cols, output_size, output_skip));
}

/*
 * The private constructor
 */
matrix_deinterleaver_soft_impl::matrix_deinterleaver_soft_impl(int rows,
                                                               int cols,
                                                               int output_size,
                                                               int output_skip)
    : gr::block("matrix_deinterleaver_soft",
                gr::io_signature::make(0, 0, 0),
                gr::io_signature::make(0, 0, 0)),
      d_rows(rows),
      d_cols(cols),
      d_output_size(output_size),
      d_output_skip(output_skip)
{
    if (d_output_size + d_output_skip > d_rows * d_cols) {
        throw std::runtime_error("Invalid size parameters for matrix deinterleave");
    }

    d_out.resize(d_rows * d_cols);

    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"),
                    boost::bind(&matrix_deinterleaver_soft_impl::msg_handler, this, _1));
}

/*
 * Our virtual destructor.
 */
matrix_deinterleaver_soft_impl::~matrix_deinterleaver_soft_impl() {}

void matrix_deinterleaver_soft_impl::forecast(int noutput_items,
                                              gr_vector_int& ninput_items_required)
{
}

int matrix_deinterleaver_soft_impl::general_work(int noutput_items,
                                                 gr_vector_int& ninput_items,
                                                 gr_vector_const_void_star& input_items,
                                                 gr_vector_void_star& output_items)
{
    return 0;
}


void matrix_deinterleaver_soft_impl::msg_handler(pmt::pmt_t pmt_msg)
{
    size_t length(0);
    auto data = pmt::f32vector_elements(pmt::cdr(pmt_msg), length);

    if (length != d_rows * d_cols)
        return;

    // Full matrix deinterleave, ignoring output cropping
    for (size_t i = 0; i < length; ++i) {
        d_out[i] = data[d_rows * (i % d_cols) + i / d_cols];
    }

    // Output cropping
    message_port_pub(
        pmt::mp("out"),
        pmt::cons(pmt::PMT_NIL,
                  pmt::init_f32vector(d_output_size, &d_out[d_output_skip])));
}


} /* namespace satellites */
} /* namespace gr */
