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
import array

class telemetry_primaryheader_adder(gr.basic_block):
    """
    docstring for block telemetry_primaryheader_adder
    """
    def __init__(self, transfer_frame_version_number, spacecraft_id, virtual_channel_id, ocf_flag, master_channel_frame_count,
                 virtual_channel_frame_count, transfer_frame_secondary_header_flag, synch_flag, packet_order_flag, segment_length_id,
                 first_header_pointer):
        gr.basic_block.__init__(self,
            name="telemetry_primaryheader_adder",
            in_sig=[],
            out_sig=[])

        ##################################################
        # Parameters
        ##################################################
        self.transfer_frame_version_number = transfer_frame_version_number
        self.spacecraft_id = spacecraft_id
        self.virtual_channel_id = virtual_channel_id
        self.ocf_flag = ocf_flag
        self.master_channel_frame_count = master_channel_frame_count
        self.virtual_channel_frame_count = virtual_channel_frame_count
        self.transfer_frame_secondary_header_flag = transfer_frame_secondary_header_flag
        self.synch_flag = synch_flag
        self.packet_order_flag = packet_order_flag
        self.segment_length_id = segment_length_id
        self.first_header_pointer = first_header_pointer

        ##################################################
        # Blocks
        ##################################################
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    PrimaryHeader = BitStruct('transfer_frame_version_number' / BitsInteger(2),
                              'spacecraft_id' / BitsInteger(10),
                              'virtual_channel_id' / BitsInteger(3),
                              'ocf_flag' / Flag,
                              'master_channel_frame_count' / BitsInteger(8),
                              'virtual_channel_frame_count' / BitsInteger(8),
                              'transfer_frame_secondary_header_flag' / Flag,
                              'synch_flag' / Flag,
                              'packet_order_flag' / Flag,
                              'segment_length_id' / BitsInteger(2),
                              'first_header_pointer' / BitsInteger(11))
    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = pmt.u8vector_elements(msg)
        finalHeader = array.array('B', telemetry.PrimaryHeader.build(dict(transfer_frame_version_number = self.transfer_frame_version_number, spacecraft_id = self.spacecraft_id,
                                                                          virtual_channel_id = self.virtual_channel_id,
                                                                          ocf_flag = self.ocf_flag,
                                                                          master_channel_frame_count = self.master_channel_frame_count,
                                                                          virtual_channel_frame_count = self.virtual_channel_frame_count,
                                                                          transfer_frame_secondary_header_flag = self.transfer_frame_secondary_header_flag,
                                                                          synch_flag = self.synch_flag,
                                                                          packet_order_flag = self.packet_order_flag,
                                                                          segment_length_id = self.segment_length_id,
                                                                          first_header_pointer = self.first_header_pointer)))

        finalPacket = numpy.append(finalHeader, packet)
        finalPacket = array.array('B', finalPacket[:])
        finalPacket = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(finalPacket), finalPacket))
        self.message_port_pub(pmt.intern('out'), finalPacket)
