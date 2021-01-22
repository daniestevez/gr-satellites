/* -*- c++ -*- */
/*
 * Copyright 2018 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_DESCRAMBLER308_H
#define INCLUDED_SATELLITES_DESCRAMBLER308_H

#include <gnuradio/sync_block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief <+description of block+>
 * \ingroup outernet
 *
 */
class SATELLITES_API descrambler308 : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<descrambler308> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::descrambler308.
     *
     * To avoid accidental use of raw pointers, satellites::descrambler308's
     * constructor is in a private implementation
     * class. satellites::descrambler308::make is the public interface for
     * creating new instances.
     */
    static sptr make();
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_DESCRAMBLER308_H */
