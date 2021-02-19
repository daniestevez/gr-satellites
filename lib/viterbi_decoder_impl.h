/* -*- c++ -*- */
/*
 * Copyright 2021 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_VITERBI_DECODER_IMPL_H
#define INCLUDED_SATELLITES_VITERBI_DECODER_IMPL_H

#include "viterbi/viterbi.h"

#include <satellites/viterbi_decoder.h>

namespace gr {
namespace satellites {

class viterbi_decoder_impl : public viterbi_decoder
{
private:
    ViterbiCodec d_codec;

public:
    viterbi_decoder_impl(int constraint, const std::vector<int>& polynomials);
    ~viterbi_decoder_impl();

    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items);

    void msg_handler(pmt::pmt_t pmt_msg);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_VITERBI_DECODER_IMPL_H */
