/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_MESSAGE_COUNTER_H
#define INCLUDED_SATELLITES_MESSAGE_COUNTER_H

#include <gnuradio/sync_block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief Counts messages
 * \ingroup satellites
 *
 * \details
 * The Message Counter block counts messages that cross the block and outputs a
 * message every time that a new message have crossed the block. The message
 * contains the count.
 */
class SATELLITES_API message_counter : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<message_counter> sptr;

    /*!
     * \brief Build a Message Counter block.
     */
    static sptr make();
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_MESSAGE_COUNTER_H */
