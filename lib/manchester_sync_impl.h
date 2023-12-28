/* -*- c++ -*- */
/*
 * Copyright 2023 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_MANCHESTER_SYNC_IMPL_H
#define INCLUDED_SATELLITES_MANCHESTER_SYNC_IMPL_H

#include <satellites/manchester_sync.h>
#include <volk/volk_alloc.hh>

namespace gr {
namespace satellites {

template <class T>
class manchester_sync_impl : public manchester_sync<T>
{
private:
    volk::vector<T> d_diffs_0;
    volk::vector<T> d_diffs_1;
    volk::vector<float> d_abs;

    static inline void compute_diff(T* out, const T* in, int block_size);
    static inline void compute_abs(float* out, const T* in, int block_size);

public:
    manchester_sync_impl(int block_size);
    ~manchester_sync_impl() override;

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items) override;
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_MANCHESTER_SYNC_IMPL_H */
