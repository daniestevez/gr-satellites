/* -*- c++ -*- */
/*
 * Copyright 2019 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_DECODE_RA_CODE_H
#define INCLUDED_SATELLITES_DECODE_RA_CODE_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief <+description of block+>
 * \ingroup satellites
 *
 */
class SATELLITES_API decode_ra_code : virtual public gr::block
{
public:
    typedef boost::shared_ptr<decode_ra_code> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::decode_ra_code.
     *
     * To avoid accidental use of raw pointers, satellites::decode_ra_code's
     * constructor is in a private implementation
     * class. satellites::decode_ra_code::make is the public interface for
     * creating new instances.
     */
    static sptr make(int size);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_DECODE_RA_CODE_H */
