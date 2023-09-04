/* -*- c++ -*- */
/*
 * Copyright 2023 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_MANCHESTER_SYNC_H
#define INCLUDED_SATELLITES_MANCHESTER_SYNC_H

#include <gnuradio/sync_decimator.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief Detects phase of a Manchester clock and integrates symbols
 * \ingroup satellites
 *
 * \details
 * The Manchester Sync block operates on a Manchester coded signal at
 * two samples per symbol (one sample per each half of the Manchester
 * pulse). The block detects which is the phase of the Manchester clock
 * (i.e., what are the symbol boundaries), integrates symbols by
 * subtracting the appropriate halves, and outputs the symbols at one
 * sample per symbol.
 *
 * The detection of the Manchester clock phase is done using a high
 * SNR approximation to the maximum likelihood metric. Detection is
 * done blockwise, with the size of the block indicated in the constructor.
 */
template <class T>
class SATELLITES_API manchester_sync : virtual public gr::sync_decimator
{
public:
    typedef boost::shared_ptr<manchester_sync<T>> sptr;

    /*!
     * \brief Constructs a Manchester Sync block.
     *
     * \param block_size Size of the block for metric evaluation (in symbols).
     */
    static sptr make(int block_size);
};

typedef manchester_sync<gr_complex> manchester_sync_cc;
typedef manchester_sync<float> manchester_sync_ff;

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_MANCHESTER_SYNC_H */
