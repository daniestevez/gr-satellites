/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_NANCOM_GOLAY_DECODE_LENGTH_H
#define INCLUDED_SATELLITES_NANCOM_GOLAY_DECODE_LENGTH_H

#include <gnuradio/sync_block.h>
#include <satellites/api.h>
#include <string>

namespace gr {
namespace satellites {

/*!
 * \brief Decodes Golay field in NanoCom packets and adds a length tag
 * \ingroup satellites
 *
 * \details
 * This block acts as a sync block on a stream of unpacked bits. Whenever a tag
 * marking the start of a Golay field is found, the block reads the 24 bits
 * following the tag, attempts to perform Golay decoding, and if successful
 * extracts the length field, computes the length in bits of the packet
 * including the Golay field, and adds a tag with this length to the beginning
 * of the Golay field so that the whole packet can be extracted as a PDU using
 * this length tag.
 */
class SATELLITES_API nanocom_golay_decode_length : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<nanocom_golay_decode_length> sptr;

    /*!
     * \brief Build the NanoCom Golay Decode Length block.
     *
     * \param golay_start_tag_key Key of the tag marking the start of Golay fields
     * \param length_tag_key Key of the tag indicating the packet length
     */
    static sptr make(const std::string& golay_start_tag_key,
                     const std::string& length_tag_key);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_NANOCOM_GOLAY_DECODE_LENGTH_H */
