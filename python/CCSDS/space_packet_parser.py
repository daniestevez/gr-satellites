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

    def __init__(self, time_header, time_format, ascii_dec_num, add_z_terminator):
        gr.basic_block.__init__(self,
                                name="space_packet_parser",
                                in_sig=[],
                                out_sig=[])
        self.time_header = time_header
        self.time_format = time_format
        self.ascii_dec_num = ascii_dec_num
        self.add_z_terminator = add_z_terminator
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = bytearray(pmt.u8vector_elements(msg))
        if self.pfield_exists == 1:
            packet_formats = [space_packet.FullPacketCUCWithPField, space_packet.FullPacketCDSWithPField,
                              space_packet.FullPacketCCSWithPField]
        else:
            packet_formats = [space_packet.FullPacketCUCNoPField, space_packet.FullPacketCDSNoPField,
                              space_packet.FullPacketCCSNoPField]

        packet_formats.extend([space_packet.FullPacketASCIIA, space_packet.FullPacketASCIIB,
                              space_packet.FullPacketNoTimeStamp])
        try:
            if self.time_header == 0:
                try:
                    packet_format = packet_formats[self.time_format]
                except IndexError:
                    print "Time Format Unknown"
                    return
            else:
                packet_format = packet_formats[5]

            if self.pfield_exists == 0 and self.time_format <= 2:
                if self.time_format == 0:
                    data = packet_format.parse(packet[:], num_of_basic_time_units = self.num_of_basic_time_units, num_of_fractional_time_units = self.num_of_fractional_time_units)
                elif self.time_format == 1:
                    data = packet_format.parse(packet[:], length_of_day_segment = self.length_of_day_segment, length_of_submillisecond_segment = self.length_of_submillisecond_segment)
                else:
                    data = packet_format.parse(packet[:], calendar_variation_flag = self.calendar_variation_flag, resolution = self.resolution)
            else:
                if self.time_header == 0 and self.time_format > 2:
                    if self.ascii_dec_num < 0 or self.ascii_dec_num > 6:
                        print
                        "Decimals of ASCII in Space Packet Parser block should be between 0 and 6. The number was automatically set to 1."
                        self.ascii_dec_num = 1
                    data = packet_format.parse(packet[:], number_of_decimals=self.ascii_dec_num, add_Z=self.add_z_terminator)
                else:
                    data = packet_format.parse(packet[:])
        except:
            print "Could not decode space packet"
            return
        print(data)