/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_U482C_ENCODE_H
#define INCLUDED_SATELLITES_U482C_ENCODE_H

#include <gnuradio/sync_block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief U482C Encoder
 * \ingroup satellites
 *
 * This block is the opposite of u482c_encode. It performs frame encoding for
 * the legacy U482C and some modes of the AX100. Input/output is PDUs.  The main
 * characteristic of the frame format implemented by this block is a 24-bit
 * header that is Golay (24, 12) encoded and contains the length of the payload
 * and some flags about the encoding.
 */
class SATELLITES_API u482c_encode : virtual public gr::sync_block
{
public:
    typedef boost::shared_ptr<u482c_encode> sptr;

    /*!
     * \brief Create a U482C Encoder.
     *
     * \param convolutional Enable convolutional encoding (not supported)
     * \param scrambler Enable CCSDS scrambling
     * \param rs Enable Reed-Solomon encoding
     * \param preamble_len Number of 0xAA bytes to add as preamble
     * \param flags_in_golay Add flags in Golay field
     */
    static sptr make(bool convolutional,
                     bool scrambler,
                     bool rs,
                     int preamble_len,
                     bool flags_in_golay);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_U482C_ENCODE_H */
