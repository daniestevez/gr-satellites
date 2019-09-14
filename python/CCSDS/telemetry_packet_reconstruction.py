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
import telemetry
import space_packet
class telemetry_packet_reconstruction(gr.basic_block):
    """
    docstring for block telemetry_packet_reconstruction
    """
    def __init__(self, packet):
        gr.basic_block.__init__(self,
            name="telemetry_packet_reconstruction",
            in_sig=[],
            out_sig=[])

        self.packet = packet
        self.last_packet = []
        self.length_of_space_packet = 0
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

        parsed = telemetry.FullPacket.parse(packet[:], size=self.calculateSize())

        if parsed.first_header_pointer == 0x3ff:
            self.last_packet.extend(packet[:])
        elif parsed.first_header_pointer == 0 and len(self.last_packet) != 0:
            self.sendPacket()
        else:
            



        if parsed.first_header_pointer != 0 and parsed.first_header_pointer != 0x3ff:
            self.last_packet.extend(packet[:parsed.first_header_pointer])
            packet = packet[parsed.first_header_pointer:]
            self.sendPacket(self.last_packet)
            primary_header = space_packet.PrimaryHeader.parse(packet[:])
            self.last_packet = packet[:primary_header.data_length+6]

        elif parsed.first_header_pointer == 0x3ff:
            self.last_packet.extend(packet[:parsed.first_header_pointer])

            space_packet_parsed = space_packet.PrimaryHeader.parse()

    def calculateSize(self):
        if self.coding == 0 or self.coding == 1:
            size = self.num_of_octets
        elif self.coding == 2:
            size = self.reed_solomon
        elif self.coding == 3:
            size = self.concatenated
        size = 4
        return size

    def sendPacket(self):
        packet = self.last_packet
        packet = array.array('B', packet[:])
        packet = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet))
        self.message_port_pub(pmt.intern('out'), packet)
        self.length_of_space_packet = 0
        self.last_packet = []
