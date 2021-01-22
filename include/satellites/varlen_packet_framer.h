/* -*- c++ -*- */
/*
 * Copyright 2017 Glenn Richardson <glenn@spacequest.com>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_VARLEN_PACKET_FRAMER_H
#define INCLUDED_VARLEN_PACKET_FRAMER_H

#include <gnuradio/block.h>
#include <gnuradio/endianness.h>
#include <pmt/pmt.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {
/*!
 * \brief insert a packet length field into a tagged stream
 * \ingroup satellites
 *
 * \details
 * input: stream of bits (unpacked bytes) with packet_len tags
 * output: a tagged stream of bits containing field length + packet bits
 *
 * This block prepends a packet length field into a tagged stream.
 *
 */
class SATELLITES_API varlen_packet_framer : virtual public gr::block
{
public:
    typedef std::shared_ptr<varlen_packet_framer> sptr;

    /*!
     * \param packet_key        tag key used to mark packets
     * \param length_field_size size of the packet length header
     * \param endianness        header inserted msb or lsb
     * \param use_golay         compute 24-bit golay header from 12-bit length
     * \param sync_word         optional pre-header sync pattern
     */
    static sptr make(const std::string& packet_key,
                     int length_field_size,
                     endianness_t endianness,
                     bool use_golay,
                     const std::vector<uint8_t> sync_word);
};

} // namespace satellites
} // namespace gr

#endif
