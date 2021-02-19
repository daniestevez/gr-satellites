/* -*- c++ -*- */
/*
 * Copyright 2021 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_VITERBI_DECODER_H
#define INCLUDED_SATELLITES_VITERBI_DECODER_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief Viterbi decoder
 * \ingroup satellites
 *
 */
class SATELLITES_API viterbi_decoder : virtual public gr::block
{
public:
    typedef std::shared_ptr<viterbi_decoder> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::viterbi_decoder.
     *
     * To avoid accidental use of raw pointers, satellites::viterbi_decoder's
     * constructor is in a private implementation
     * class. satellites::viterbi_decoder::make is the public interface for
     * creating new instances.
     */
    static sptr make(int constraint, const std::vector<int>& polynomials);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_VITERBI_DECODER_H */
