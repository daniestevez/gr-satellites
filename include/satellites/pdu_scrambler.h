/* -*- c++ -*- */
/*
 * Copyright 2022 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_PDU_SCRAMBLER_H
#define INCLUDED_SATELLITES_PDU_SCRAMBLER_H

#include <gnuradio/block.h>
#include <satellites/api.h>
#include <vector>

namespace gr {
namespace satellites {

/*!
 * \brief PDU Scrambler
 * \ingroup satellites
 *
 * \details
 * Uses a predefined sequence to implement a synchronous scrambler that acts
 * on PDUs. The scrambling sequence needs to be longer than the PDUs that the
 * block will process. PDUs which are longer than the sequence are dropped.
 */
class SATELLITES_API pdu_scrambler : virtual public gr::block
{
public:
    typedef boost::shared_ptr<pdu_scrambler> sptr;

    /*!
     * \brief Build the PDU Scrambler block.
     *
     * \param sequence The scrambling sequence to use.
     */
    static sptr make(const std::vector<uint8_t>& sequence);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_PDU_SCRAMBLER_H */
