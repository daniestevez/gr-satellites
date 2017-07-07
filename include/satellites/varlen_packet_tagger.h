/* -*- c++ -*- */
/*
 * Copyright 2017 Glenn Richardson <glenn@spacequest.com> 
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>
 */

#ifndef INCLUDED_VARLEN_PACKET_TAGGER_H
#define INCLUDED_VARLEN_PACKET_TAGGER_H

#include <satellites/api.h>
#include <gnuradio/block.h>
#include <gnuradio/endianness.h>
#include <pmt/pmt.h>

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
      static sptr make(const std::string &sync_key,
                       const std::string &packet_key,
                       int length_field_size,
                       int max_packet_size,
                       endianness_t endianness,
                       bool use_golay);
    };

  } // namespace satellites
} // namespace gr

#endif

