/* -*- c++ -*- */
/*
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_NUSAT_DECODER_H
#define INCLUDED_SATELLITES_NUSAT_DECODER_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief <+description of block+>
 * \ingroup satellites
 *
 */
class SATELLITES_API nusat_decoder : virtual public gr::block
{
public:
    typedef boost::shared_ptr<nusat_decoder> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::nusat_decoder.
     *
     * To avoid accidental use of raw pointers, satellites::nusat_decoder's
     * constructor is in a private implementation
     * class. satellites::nusat_decoder::make is the public interface for
     * creating new instances.
     */
    static sptr make();
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_NUSAT_DECODER_H */
