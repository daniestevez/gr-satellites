/* -*- c++ -*- */
/*
 * Copyright 2023 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "manchester_sync_impl.h"
#include <gnuradio/io_signature.h>
#include <volk/volk.h>
#include <cmath>
#include <cstring>

namespace gr {
namespace satellites {

template <class T>
typename manchester_sync<T>::sptr manchester_sync<T>::make(int block_size)
{
    return gnuradio::get_initial_sptr(new manchester_sync_impl<T>(block_size));
}


template <class T>
manchester_sync_impl<T>::manchester_sync_impl(int block_size)
    : gr::sync_decimator("manchester_sync",
                         gr::io_signature::make(1, 1, sizeof(T)),
                         gr::io_signature::make(1, 1, sizeof(T)),
                         2)
{
    this->d_diffs_0.resize(block_size);
    this->d_diffs_1.resize(block_size);
    this->d_abs.resize(block_size);
    this->set_history(2);
    this->set_output_multiple(block_size);
}

template <class T>
manchester_sync_impl<T>::~manchester_sync_impl()
{
}

template <class T>
int manchester_sync_impl<T>::work(int noutput_items,
                                  gr_vector_const_void_star& input_items,
                                  gr_vector_void_star& output_items)
{
    auto in = static_cast<const T*>(input_items[0]);
    auto out = static_cast<T*>(output_items[0]);

    const int block_size = d_diffs_0.size();

    for (int j = 0; j < noutput_items; j += block_size) {
        compute_diff(&d_diffs_0[0], &in[2 * j], block_size);
        compute_diff(&d_diffs_1[0], &in[2 * j + 1], block_size);
        compute_abs(&d_abs[0], &d_diffs_0[0], block_size);
        float metric0;
        volk_32f_accumulator_s32f(&metric0, &d_abs[0], block_size);
        compute_abs(&d_abs[0], &d_diffs_1[0], block_size);
        float metric1;
        volk_32f_accumulator_s32f(&metric1, &d_abs[0], block_size);
        const auto diff = metric0 > metric1 ? &d_diffs_0[0] : &d_diffs_1[0];
        std::memcpy(&out[j], diff, block_size * sizeof(T));
    }

    return noutput_items;
}

template <class T>
void manchester_sync_impl<T>::compute_diff(T* out, const T* in, int block_size)
{
    for (int j = 0; j < block_size; ++j) {
        out[j] = 0.5f * (in[2 * j] - in[2 * j + 1]);
    }
}

template <>
void manchester_sync_impl<gr_complex>::compute_abs(float* out,
                                                   const gr_complex* in,
                                                   int block_size)
{
    volk_32fc_magnitude_32f(out, in, block_size);
}

template <>
void manchester_sync_impl<float>::compute_abs(float* out, const float* in, int block_size)
{
    // There is no Volk kernel for abs of 32f
    for (int j = 0; j < block_size; ++j) {
        out[j] = fabsf(in[j]);
    }
}

template class manchester_sync<gr_complex>;
template class manchester_sync<float>;

} /* namespace satellites */
} /* namespace gr */
