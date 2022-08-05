/* -*- c++ -*- */
/*
 * Copyright 2022 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_PHASE_UNWRAP_H
#define INCLUDED_SATELLITES_PHASE_UNWRAP_H

#include <gnuradio/sync_block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief Unwraps a phase time series.
 * \ingroup satellites
 *
 * \details
 * The Phase Unwrap block unwraps a phase input by counting integer cycles. The
 * integer number of cycles is given as an int64_t, so that overflows are
 * impossible in most use cases. The output of the block is a vector of 12 bytes
 * that contains the integer number of cycles in the first 8 bytes and the
 * fractional phase in radians in the last 4 bytes.
 */
class SATELLITES_API phase_unwrap : virtual public gr::sync_block
{
public:
    typedef boost::shared_ptr<phase_unwrap> sptr;

    /*!
     * \brief Build the Phase Unwrap block
     */
    static sptr make();
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_PHASE_UNWRAP_H */
