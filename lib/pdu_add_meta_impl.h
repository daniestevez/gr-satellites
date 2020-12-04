/* -*- c++ -*- */
/*
 * Copyright 2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_PDU_ADD_META_IMPL_H
#define INCLUDED_SATELLITES_PDU_ADD_META_IMPL_H

#include <satellites/pdu_add_meta.h>

namespace gr {
namespace satellites {

class pdu_add_meta_impl : public pdu_add_meta
{
private:
    pmt::pmt_t d_meta;

public:
    pdu_add_meta_impl(pmt::pmt_t meta);
    ~pdu_add_meta_impl();

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

#endif /* INCLUDED_SATELLITES_PDU_ADD_META_IMPL_H */
