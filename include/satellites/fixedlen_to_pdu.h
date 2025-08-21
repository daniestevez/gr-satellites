/* -*- c++ -*- */
/*
 * Copyright 2022,2025 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_FIXEDLEN_TO_PDU_H
#define INCLUDED_SATELLITES_FIXEDLEN_TO_PDU_H

#include <gnuradio/pdu.h>
#include <gnuradio/sync_block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief Fixedlen to PDU
 * \ingroup satellites
 *
 *  Extracts PDUs of fixed maximum length according to syncword tags.
 *
 *  Given an input stream containing tags that mark the location of frames, this
 *  block extracts PDUs starting at the location of those tags. The length of
 *  the PDUs is determined by either the presence of a packet length tag, if a
 *  key for this tag has been specified and such tag is present in the first
 *  item of the frame, or by the maximum packet length otherwise.  The data in
 *  the PDUs may overlap if tags are spaced less than the PDU length.
 */
class SATELLITES_API fixedlen_to_pdu : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<fixedlen_to_pdu> sptr;

    /*!
     * Make a Fixedlen to PDU block.
     *
     * \param type Input stream type.
     * \param syncword_tag Name of the syncword tags to use.
     * \param packet_len Maximum PDU length, in items of the input stream.
     * \param pack When the input type is bytes and this option is enabled,
       8 bits per byte are packed in the output PDU. The packet length should
       correspond to the number of bits, and be a multiple of 8.
     * \param packet_len_tag_key Key of the syncword tag to use for packet length.
       If this key is empty, the max packet length is used for all the packets.
     */
    static sptr make(types::vector_type type,
                     const std::string& syncword_tag,
                     size_t packet_len,
                     bool pack = false,
                     const std::string& packet_len_tag_key = "");
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_FIXEDLEN_TO_PDU_H */
