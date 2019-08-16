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

    """

    def __init__(self, time_header, time_format):
        gr.basic_block.__init__(self,
                                name="space_packet_parser",
                                in_sig=[],
                                out_sig=[])
        self.time_header = time_header
        self.time_format = time_format
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = bytearray(pmt.u8vector_elements(msg))
        try:
            if self.time_header == 0:
                if self.time_format == 0:
                    data = space_packet.FullPacketCUC.parse(packet[:])
                elif self.time_format == 1:
                    data = space_packet.FullPacketCDS.parse(packet[:])
                elif self.time_format == 2:
                    data = space_packet.FullPacketCCS.parse(packet[:])
                elif self.time_format == 3:
                    data = space_packet.FullPacketASCIIA.parse(packet[:])
                elif self.time_format == 4:
                    data = space_packet.FullPacketASCIIB.parse(packet[:])
                else:
                    print "Time Format Unknown"
            else:
                data = space_packet.FullPacketNoTimeStamp.parse(packet[:])
        except:
            print "Could not decode space packet"
            return
        print(data)