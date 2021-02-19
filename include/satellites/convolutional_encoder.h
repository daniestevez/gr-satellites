/* -*- c++ -*- */
/*
 * Copyright 2021 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_CONVOLUTIONAL_ENCODER_H
#define INCLUDED_SATELLITES_CONVOLUTIONAL_ENCODER_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief Convolutional encoder
 * \ingroup satellites
 *
 */
class SATELLITES_API convolutional_encoder : virtual public gr::block
{
public:
    typedef std::shared_ptr<convolutional_encoder> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::convolutional_encoder.
     *
     * To avoid accidental use of raw pointers, satellites::convolutional_encoder's
     * constructor is in a private implementation
     * class. satellites::convolutional_encoder::make is the public interface for
     * creating new instances.
     */
    static sptr make(int constraint, const std::vector<int>& polynomials);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_CONVOLUTIONAL_ENCODER_H */
