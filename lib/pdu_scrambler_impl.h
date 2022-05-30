/* -*- c++ -*- */
/*
 * Copyright 2022 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_PDU_SCRAMBLER_IMPL_H
#define INCLUDED_SATELLITES_PDU_SCRAMBLER_IMPL_H

#include <satellites/pdu_scrambler.h>
#include <vector>

namespace gr {
namespace satellites {

class pdu_scrambler_impl : public pdu_scrambler
{
private:
    const std::vector<uint8_t> d_sequence;

public:
    pdu_scrambler_impl(const std::vector<uint8_t>& sequence);
    ~pdu_scrambler_impl();

    void forecast(int noutput_items, gr_vector_int& ninput_items_required);

    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items);

    void msg_handler(pmt::pmt_t pmt_msg);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_PDU_SCRAMBLER_IMPL_H */
