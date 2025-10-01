/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_PACKET_CSMA_H
#define INCLUDED_SATELLITES_PACKET_CSMA_H

#include <gnuradio/block.h>
#include <satellites/api.h>
#include <string>

namespace gr {
namespace satellites {

/*!
 * \brief Passes packets to the output only when carrier sense is not triggering
 * \ingroup satellites
 *
 * \details
 *
 * This block implements a CSMA system for a stream of packets delimited by
 * packet_len tags. The block expects to receive messages from a carrier sense
 * detector that indicate the current carrier sense state every time that the
 * state changes. These messages should be a pair containing a bool in the cdr.
 *
 * Whenever a new packet arrives to this block, the current status of the
 * carrier sense is checked, and the packet is only propagated to the output if
 * the carrier sense is false. Otherwise the packet is retained until carrier
 * sense becomes false.
 *
 * As an exception to this rule, if 'back_to_back_priority' is set to true and a
 * packet arrives back-to-back (meaning that it begins in the same work() call
 * as the end of the previous packet), then the packet is propagated to the
 * output immediately regardless of the current state of the carrier sense. This
 * is mainly intended as a workaround for systems in which the carrier sense
 * might detect the packets transmitted by this system due to TX to RX leakage.
 *
 */
class SATELLITES_API packet_csma : virtual public gr::block
{
public:
    typedef std::shared_ptr<packet_csma> sptr;

    /*!
     * \brief Build the Level to Packet CSMA block.
     *
     * \param itemsize Size of the items in bytes.
     * \param back_to_back_priority Transmit back-to-back packets ignoring the
     *   carrier sense.
     * \param len_tag_key Packet length key of the tagged stream.
     */
    static sptr make(size_t itemsize,
                     bool back_to_back_priority,
                     const std::string& len_tag_key = "packet_len");
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_PACKET_CSMA_H */
