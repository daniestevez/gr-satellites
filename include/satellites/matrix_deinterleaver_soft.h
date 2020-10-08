/* -*- c++ -*- */
/*
 * Copyright 2019 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_MATRIX_DEINTERLEAVER_SOFT_H
#define INCLUDED_SATELLITES_MATRIX_DEINTERLEAVER_SOFT_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief <+description of block+>
 * \ingroup satellites
 *
 */
class SATELLITES_API matrix_deinterleaver_soft : virtual public gr::block
{
public:
    typedef boost::shared_ptr<matrix_deinterleaver_soft> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of
     * satellites::matrix_deinterleaver_soft.
     *
     * To avoid accidental use of raw pointers, satellites::matrix_deinterleaver_soft's
     * constructor is in a private implementation
     * class. satellites::matrix_deinterleaver_soft::make is the public interface for
     * creating new instances.
     */
    static sptr make(int rows, int cols, int output_size, int output_skip);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_MATRIX_DEINTERLEAVER_SOFT_H */
