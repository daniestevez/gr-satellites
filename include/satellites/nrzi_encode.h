/* -*- c++ -*- */
/*
 * Copyright 2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_NRZI_ENCODE_H
#define INCLUDED_SATELLITES_NRZI_ENCODE_H

#include <gnuradio/sync_block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief NRZI encode
 * \ingroup satellites
 *
 */
class SATELLITES_API nrzi_encode : virtual public gr::sync_block
{
public:
    typedef boost::shared_ptr<nrzi_encode> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::nrzi_encode.
     *
     * To avoid accidental use of raw pointers, satellites::nrzi_encode's
     * constructor is in a private implementation
     * class. satellites::nrzi_encode::make is the public interface for
     * creating new instances.
     */
    static sptr make();
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_NRZI_ENCODE_H */
