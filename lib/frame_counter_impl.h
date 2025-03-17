/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_FRAME_COUNTER_IMPL_H
#define INCLUDED_SATELLITES_FRAME_COUNTER_IMPL_H

#include <pmt/pmt.h>
#include <satellites/frame_counter.h>
#include <cstdint>

namespace gr {
namespace satellites {

class frame_counter_impl : public frame_counter
{
private:
    const size_t d_itemsize;
    const size_t d_frame_size;
    const pmt::pmt_t d_count_port;
    uint64_t d_count = 0;
    uint64_t d_last = 0;

public:
    frame_counter_impl(size_t itemsize, size_t frame_size);
    ~frame_counter_impl();

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_FRAME_COUNTER_IMPL_H */
