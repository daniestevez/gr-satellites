/* -*- c++ -*- */
/*
 * Copyright 2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "pdu_add_meta_impl.h"
#include <gnuradio/io_signature.h>

#include <algorithm>
#include <vector>

namespace gr {
namespace satellites {

pdu_add_meta::sptr pdu_add_meta::make(pmt::pmt_t meta)
{
    return gnuradio::get_initial_sptr(new pdu_add_meta_impl(meta));
}

/*
 * The private constructor
 */
pdu_add_meta_impl::pdu_add_meta_impl(pmt::pmt_t meta)
    : gr::block("pdu_add_meta",
                gr::io_signature::make(0, 0, 0),
                gr::io_signature::make(0, 0, 0)),
      d_meta(meta)
{
    message_port_register_out(pmt::mp("out"));
    message_port_register_in(pmt::mp("in"));
    set_msg_handler(pmt::mp("in"), [this](pmt::pmt_t msg) { this->msg_handler(msg); });
}

/*
 * Our virtual destructor.
 */
pdu_add_meta_impl::~pdu_add_meta_impl() {}

void pdu_add_meta_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
{
}

int pdu_add_meta_impl::general_work(int noutput_items,
                                    gr_vector_int& ninput_items,
                                    gr_vector_const_void_star& input_items,
                                    gr_vector_void_star& output_items)
{
    return 0;
}

void pdu_add_meta_impl::msg_handler(pmt::pmt_t pmt_msg)
{
    pmt::pmt_t car = pmt::car(pmt_msg);
    if (car == pmt::PMT_NIL) {
        car = pmt::make_dict();
    }
    car = pmt::dict_update(car, d_meta);

    message_port_pub(pmt::mp("out"), pmt::cons(car, pmt::cdr(pmt_msg)));
}

} /* namespace satellites */
} /* namespace gr */
