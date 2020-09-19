/* -*- c++ -*- */
/*
 * Copyright 2019 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_DISTRIBUTED_SYNCFRAME_SOFT_H
#define INCLUDED_SATELLITES_DISTRIBUTED_SYNCFRAME_SOFT_H

#include <gnuradio/sync_block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief <+description of block+>
 * \ingroup satellites
 *
 */
class SATELLITES_API distributed_syncframe_soft : virtual public gr::sync_block
{
public:
    typedef boost::shared_ptr<distributed_syncframe_soft> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of
     * satellites::distributed_syncframe_soft.
     *
     * To avoid accidental use of raw pointers, satellites::distributed_syncframe_soft's
     * constructor is in a private implementation
     * class. satellites::distributed_syncframe_soft::make is the public interface for
     * creating new instances.
     */
    static sptr make(int threshold, const std::string& syncword, int step);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_DISTRIBUTED_SYNCFRAME_H */
