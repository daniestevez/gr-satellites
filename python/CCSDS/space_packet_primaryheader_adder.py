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
    def __init__(self, ccsds_version, packet_type, secondary_header_flag, AP_ID, sequence_flags, packet_sequence_count,
                 data_length):
        gr.basic_block.__init__(self,
            name="space_packet_primaryheader_adder",
            in_sig=[],
            out_sig=[])

        ##################################################
        # Parameters
        ##################################################
        self.ccsds_version = ccsds_version
        self.packet_type = packet_type
        self.secondary_header_flag = secondary_header_flag
        self.AP_ID = AP_ID
        self.sequence_flags = sequence_flags
        self.packet_sequence_count = packet_sequence_count
        self.data_length = data_length

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
        header = numpy.array([self.ccsds_version, self.packet_type, self.secondary_header_flag, self.AP_ID,
        self.sequence_flags, self.packet_sequence_count, self.data_length])
        finalHeader = numpy.array(numpy.zeros(6), dtype = int)
        finalHeader[0] = (int(bin(header[0]),2) << 5) + (int(bin(header[1]),2) << 4) + (int(bin(header[2]),2) << 3)
        if header[3] > 128:
            finalHeader[0] += int(bin(header[3]),2) >> 8
            finalHeader[1] = int(bin(header[3])[5:].zfill(8), 2)
        else:
            finalHeader[1] = int(bin(header[3]), 2)

        finalHeader[2] = (int(bin(header[4]),2) << 6)
        if header[5] > 128:
            finalHeader[2] += int(bin(header[5]),2)  >> 8
            finalHeader[3] = int(bin(header[5])[8:].zfill(8), 2)
        else:
            finalHeader[3] = int(bin(header[5]), 2)

        if header[6] > 128:
            finalHeader[4] = int(bin(header[6]), 2) >> 8
            finalHeader[5] = int(bin(header[6])[8:].zfill(8), 2)
        else:
            finalHeader[4] = 0
            finalHeader[5] = int(bin(header[6]), 2)

        finalPacket = numpy.append(finalHeader, packet)
        finalPacket = array.array('B', finalPacket[:])
        finalPacket = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(finalPacket), finalPacket))
        self.message_port_pub(pmt.intern('out'), finalPacket)

