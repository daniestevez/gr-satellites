/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_LEVEL_TO_MESSAGE_H
#define INCLUDED_SATELLITES_LEVEL_TO_MESSAGE_H

#include <gnuradio/sync_block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief Converts changes in signal level to messages
 * \ingroup satellites
 *
 * \details
 * This block is mainly intended to be used with the output of the Threshold
 * block. It compares its input with a given threshold. Whenever the input
 * crosses the threshold, a message is output saying if the signal is now over
 * the threshold or below the threshold. If there are multiple threshold
 * crossings inside a work() call, only the last one is considered, so at most
 * there is an output message per work() call (i.e., the block only ever looks
 * at the last input sample in each work() call).
 */
class SATELLITES_API level_to_message : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<level_to_message> sptr;

    /*!
     * \brief Build the Level to Message block.
     *
     * \param threshold Level change threshold
     */
    static sptr make(float threshold);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_LEVEL_TO_MESSAGE_H */
