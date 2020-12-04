/* -*- c++ -*- */
/*
 * Copyright 2018,2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_ENCODE_RS_H
#define INCLUDED_SATELLITES_ENCODE_RS_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief <+description of block+>
 * \ingroup satellites
 *
 */
class SATELLITES_API encode_rs : virtual public gr::block
{
public:
    typedef boost::shared_ptr<encode_rs> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::encode_rs.
     *
     * To avoid accidental use of raw pointers, satellites::encode_rs's
     * constructor is in a private implementation
     * class. satellites::encode_rs::make is the public interface for
     * creating new instances.
     */
    static sptr make(bool dual_basis, int interleave = 1);
    static sptr
    make(int symsize, int gfpoly, int fcr, int prim, int nroots, int interleave = 1);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_ENCODE_RS_H */
