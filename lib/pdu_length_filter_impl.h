/* -*- c++ -*- */
/*
 * Copyright 2021 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_PDU_LENGTH_FILTER_IMPL_H
#define INCLUDED_SATELLITES_PDU_LENGTH_FILTER_IMPL_H

#include <satellites/pdu_length_filter.h>

namespace gr {
namespace satellites {

class pdu_length_filter_impl : public pdu_length_filter
{
private:
    size_t d_min, d_max;

public:
    pdu_length_filter_impl(int min, int max);
    ~pdu_length_filter_impl();

    // Where all the action really happens
    void forecast(int noutput_items, gr_vector_int& ninput_items_required);

    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items);

    void msg_handler(pmt::pmt_t pmt_msg);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_PDU_LENGTH_FILTER_IMPL_H */
