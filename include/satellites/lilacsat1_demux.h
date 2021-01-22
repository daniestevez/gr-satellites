/* -*- c++ -*- */
/*
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_LILACSAT1_DEMUX_H
#define INCLUDED_SATELLITES_LILACSAT1_DEMUX_H

#include <gnuradio/sync_block.h>
#include <satellites/api.h>
#include <string>

namespace gr {
namespace satellites {

/*!
 * \brief <+description of block+>
 * \ingroup satellites
 *
 */
class SATELLITES_API lilacsat1_demux : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<lilacsat1_demux> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::lilacsat1_demux.
     *
     * To avoid accidental use of raw pointers, satellits::lilacsat1_demux's
     * constructor is in a private implementation
     * class. satellites::lilacsat1_demux::make is the public interface for
     * creating new instances.
     */
    static sptr make(std::string tag);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_LILACSAT1_DEMUX_H */
