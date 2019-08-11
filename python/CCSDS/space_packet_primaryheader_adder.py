#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Athanasios Theocharis <athatheoc@gmail.com>
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy
from gnuradio import gr
import pmt
import space_packet
import array

class space_packet_primaryheader_adder(gr.basic_block):
    """
    docstring for block space_packet_primaryheader_adder
    """
    def __init__(self, packet_type, AP_ID, count_or_name, packet_sequence_name):
        gr.basic_block.__init__(self,
            name="space_packet_primaryheader_adder",
            in_sig=[],
            out_sig=[])

        ##################################################
        # Parameters
        ##################################################
        self.ccsds_version = 0
        self.packet_type = packet_type
        self.secondary_header_flag = 0
        self.AP_ID = AP_ID
        self.sequence_flags = 3
        self.packet_sequence_count = 0
        self.packet_sequence_name = packet_sequence_name
        self.count_or_name = count_or_name
        self.data_length = 0

        ##################################################
        # Blocks
        ##################################################
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = pmt.u8vector_elements(msg)
        mask = 0b11111111 #Use this to take the last 8 bits of a number
        self.data_length = len(packet)

        if self.packet_type == 0 or self.count_or_name == 0:
            self.packet_sequence_count += 1

            header = numpy.array([self.ccsds_version, self.packet_type, self.secondary_header_flag, self.AP_ID,
                                  self.sequence_flags, self.packet_sequence_count, self.data_length])
        else:
            header = numpy.array([self.ccsds_version, self.packet_type, self.secondary_header_flag, self.AP_ID,
                                  self.sequence_flags, self.packet_sequence_name, self.data_length])

        finalHeader = numpy.array(numpy.zeros(6), dtype=int)
        finalHeader[0] = (int(bin(header[0]), 2) << 5) + (int(bin(header[1]), 2) << 4) + (int(bin(header[2]), 2) << 3)
        finalHeader[0] += int(bin(header[3]), 2) >> 8
        finalHeader[1] = int(bin(header[3] & mask), 2)
        finalHeader[2] = (int(bin(header[4]), 2) << 6)
        finalHeader[2] += int(bin(header[5]), 2) >> 8
        finalHeader[3] = int(bin(header[5] & mask), 2)
        finalHeader[4] = int(bin(header[6]), 2) >> 8
        finalHeader[5] = int(bin(header[6] & mask), 2)
        finalPacket = numpy.append(finalHeader, packet)
        finalPacket = array.array('B', finalPacket[:])
        finalPacket = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(finalPacket), finalPacket))
        self.message_port_pub(pmt.intern('out'), finalPacket)

