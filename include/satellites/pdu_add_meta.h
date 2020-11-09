/* -*- c++ -*- */
/*
 * Copyright 2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_PDU_ADD_META_H
#define INCLUDED_SATELLITES_PDU_ADD_META_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief <+description of block+>
 * \ingroup satellites
 *
 */
class SATELLITES_API pdu_add_meta : virtual public gr::block
{
public:
    typedef boost::shared_ptr<pdu_add_meta> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::pdu_add_meta.
     *
     * To avoid accidental use of raw pointers, satellites::pdu_add_meta's
     * constructor is in a private implementation
     * class. satellites::pdu_add_meta::make is the public interface for
     * creating new instances.
     */
    static sptr make(pmt::pmt_t meta);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_PDU_ADD_META_H */
