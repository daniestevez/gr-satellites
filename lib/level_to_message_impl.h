/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_LEVEL_TO_MESSAGE_IMPL_H
#define INCLUDED_SATELLITES_LEVEL_TO_MESSAGE_IMPL_H

#include <satellites/level_to_message.h>

namespace gr {
namespace satellites {

class level_to_message_impl : public level_to_message
{
private:
    const float d_threshold;
    const pmt::pmt_t d_out_port;
    const pmt::pmt_t d_above_tag;
    bool d_above_threshold = false;

public:
    level_to_message_impl(float threshold);
    ~level_to_message_impl() override;

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items) override;
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_LEVEL_TO_MESSAGE_IMPL_H */
