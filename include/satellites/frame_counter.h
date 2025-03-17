/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_FRAME_COUNTER_H
#define INCLUDED_SATELLITES_FRAME_COUNTER_H

#include <gnuradio/sync_block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief Counts frames of fixed size.
 * \ingroup satellites
 *
 * \details
 * The Frame Counter block counts frames of a fixed size that cross
 * the block and outputs a message every time that new frames have
 * crossed the block. The message contains the count.
 */
class SATELLITES_API frame_counter : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<frame_counter> sptr;

    /*!
     * \brief Build the Frame Counter block.
     *
     * \param itemsize Size of the stream items.
     * \param frame_size Size of the frames.
     */
    static sptr make(size_t itemsize, size_t frame_size);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_FRAME_COUNTER_H */
