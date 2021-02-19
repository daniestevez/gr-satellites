/* -*- c++ -*- */
/*
 * Copyright 2021 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_PDU_LENGTH_FILTER_H
#define INCLUDED_SATELLITES_PDU_LENGTH_FILTER_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief <+description of block+>
 * \ingroup satellites
 *
 */
class SATELLITES_API pdu_length_filter : virtual public gr::block
{
public:
    typedef std::shared_ptr<pdu_length_filter> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::pdu_length_filter.
     *
     * To avoid accidental use of raw pointers, satellites::pdu_length_filter's
     * constructor is in a private implementation
     * class. satellites::pdu_length_filter::make is the public interface for
     * creating new instances.
     */
    static sptr make(int min, int max);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_PDU_LENGTH_FILTER_H */
