/* -*- c++ -*- */
/*
 * Copyright 2016 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_AX100_DECODE_H
#define INCLUDED_SATELLITES_AX100_DECODE_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief <+description of block+>
 * \ingroup satellites
 *
 */
class SATELLITES_API ax100_decode : virtual public gr::block
{
public:
    typedef std::shared_ptr<ax100_decode> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::ax100_decode.
     *
     * To avoid accidental use of raw pointers, satellites::ax100_decode's
     * constructor is in a private implementation
     * class. satellites::ax100_decode::make is the public interface for
     * creating new instances.
     */
    static sptr make(bool verbose);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_AX100_DECODE_H */
