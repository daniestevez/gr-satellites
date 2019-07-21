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


class space_packet_parser(gr.basic_block):
    """
    docstring for block space_packet_parser
    """

    def __init__(self, ccsds_version, packet_type, secondary_header_flag, process_id, level_flag, payload_flag,
                 packet_category, sequence_flag, data_length):
        gr.basic_block.__init__(self,
                                name="space_packet_parser",
                                in_sig=[],
                                out_sig=[])

        ##################################################
        # Parameters
        ##################################################
        self.ccsds_version = ccsds_version
        self.packet_type = packet_type
        self.secondary_header_flag = secondary_header_flag
        self.process_id = process_id
        self.level_flag = level_flag
        self.payload_flag = payload_flag
        self.packet_category = packet_category
        self.sequence_flag = sequence_flag
        self.data_length = data_length

        ##################################################
        # Blocks
        ##################################################
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = bytearray(pmt.u8vector_elements(msg))
        try:
            data = space_packet.PayLoad.parse(packet[:], dataLength=self.data_length)
        except:
            print "Could not decode space packet"
            return
        print "ccsds_version: %d\npacket_type: %d\nsecondary_header_flag: %d\nprocess_id: %d\nlevel_flag: %d\n" \
              "payload_flag: %d\npacket_category: %d\nsequence_flag: %d\ndata_length: %d" % (self.ccsds_version, self.packet_type,
            self.secondary_header_flag, self.process_id, self.level_flag, self.payload_flag, self.packet_category,
            self.sequence_flag, self.data_length)
        print(data)
