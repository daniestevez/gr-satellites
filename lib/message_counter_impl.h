/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_MESSAGE_COUNTER_IMPL_H
#define INCLUDED_SATELLITES_MESSAGE_COUNTER_IMPL_H

#include <pmt/pmt.h>
#include <satellites/message_counter.h>
#include <cstdint>

namespace gr {
namespace satellites {

class message_counter_impl : public message_counter
{
private:
    const pmt::pmt_t d_out_port;
    const pmt::pmt_t d_count_port;
    uint64_t d_count = 0;

public:
    message_counter_impl();
    ~message_counter_impl() override;

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items) override;

    void msg_handler(const pmt::pmt_t& pmt_msg);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_MESSAGE_COUNTER_IMPL_H */
