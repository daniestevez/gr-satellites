/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_PACKET_CSMA_IMPL_H
#define INCLUDED_SATELLITES_PACKET_CSMA_IMPL_H

#include <satellites/packet_csma.h>

namespace gr {
namespace satellites {

class packet_csma_impl : public packet_csma
{
private:
    const size_t d_itemsize;
    const pmt::pmt_t d_len_tag_key;
    const bool d_back_to_back_priority;
    size_t d_remaining_items = 0;
    bool d_carrier_sense = false;

    void handle_carrier_sense(const pmt::pmt_t& pmt_msg)
    {
        d_carrier_sense = pmt::to_bool(pmt::cdr(pmt_msg));
    }

public:
    packet_csma_impl(size_t itemsize,
                     bool back_to_back_priority,
                     const std::string& len_tag_key);
    ~packet_csma_impl() override;

    void forecast(int noutput_items, gr_vector_int& ninput_items_required) override;

    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items) override;
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_PACKET_CSMA_IMPL_H */
