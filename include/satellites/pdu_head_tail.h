/* -*- c++ -*- */
/*
 * Copyright 2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_PDU_HEAD_TAIL_H
#define INCLUDED_SATELLITES_PDU_HEAD_TAIL_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief <+description of block+>
 * \ingroup satellites
 *
 */
class SATELLITES_API pdu_head_tail : virtual public gr::block
{
public:
    typedef std::shared_ptr<pdu_head_tail> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::pdu_head_tail.
     *
     * To avoid accidental use of raw pointers, satellites::pdu_head_tail's
     * constructor is in a private implementation
     * class. satellites::pdu_head_tail::make is the public interface for
     * creating new instances.
     */
    static sptr make(int mode, size_t num);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_PDU_HEAD_TAIL_H */
