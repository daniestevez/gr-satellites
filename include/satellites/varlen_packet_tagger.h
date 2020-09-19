/* -*- c++ -*- */
/*
 * Copyright 2017 Glenn Richardson <glenn@spacequest.com>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_VARLEN_PACKET_TAGGER_H
#define INCLUDED_VARLEN_PACKET_TAGGER_H

#include <gnuradio/block.h>
#include <gnuradio/endianness.h>
#include <pmt/pmt.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {
/*!
 * \brief Examine input stream for sync tags and extract packet length.
 * \ingroup satellites
 *
 * \details
 * input: stream of bits (unpacked bytes) with sync tags
 * output: a tagged stream of bits containing just the received packets
 *
 * This block uses the sync tag on the input stream to identify
 * the header of packets.  The length of each packet is extracted
 * from the stream's header.  The length of the header field and
 * the endianness are parameters.
 *
 */
class SATELLITES_API varlen_packet_tagger : virtual public gr::block
{
public:
    typedef boost::shared_ptr<varlen_packet_tagger> sptr;

    /*!
     * \param sync_key
     * \param packet_key
     * \param length_field_size
     * \param max_packet_size
     * \param endianness
     * \param use_golay For 24-bit golay headers
     */
    static sptr make(const std::string& sync_key,
                     const std::string& packet_key,
                     int length_field_size,
                     int max_packet_size,
                     endianness_t endianness,
                     bool use_golay);
};

} // namespace satellites
} // namespace gr

#endif
