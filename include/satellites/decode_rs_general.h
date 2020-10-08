/* -*- c++ -*- */
/*
 * Copyright 2018 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_DECODE_RS_GENERAL_H
#define INCLUDED_SATELLITES_DECODE_RS_GENERAL_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief <+description of block+>
 * \ingroup satellites
 *
 */
class SATELLITES_API decode_rs_general : virtual public gr::block
{
public:
    typedef boost::shared_ptr<decode_rs_general> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::decode_rs_general.
     *
     * To avoid accidental use of raw pointers, satellites::decode_rs_general's
     * constructor is in a private implementation
     * class. satellites::decode_rs_general::make is the public interface for
     * creating new instances.
     */
    static sptr make(int gfpoly, int fcr, int prim, int nroots, bool verbose);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_DECODE_RS_GENERAL_H */
