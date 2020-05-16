#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Athanasios Theocharis <athatheoc@gmail.com>
# This was made under ESA Summer of Code in Space 2019
# by Athanasios Theocharis, mentored by Daniel Estevez
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy
from gnuradio import gr
import pmt
from . import space_packet
import array

class space_packet_primaryheader_adder(gr.basic_block):
    """
    docstring for block space_packet_primaryheader_adder
    """
    def __init__(self, packet_type, secondary_header_flag, AP_ID, count_or_name, packet_sequence_name):
        gr.basic_block.__init__(self,
            name="space_packet_primaryheader_adder",
            in_sig=[],
            out_sig=[])

        ##################################################
        # Parameters
        ##################################################
        self.ccsds_version = 0
        self.packet_type = packet_type
        self.secondary_header_flag = secondary_header_flag
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
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = pmt.u8vector_elements(msg)
        self.data_length = len(packet)
        self.packet_sequence_count += 1
        count_or_name = self.packet_sequence_count if self.packet_type == 0 or self.count_or_name == 0 else self.packet_sequence_name

        finalHeader = array.array('B', space_packet.PrimaryHeader.build(dict(ccsds_version = self.ccsds_version,
                                                                packet_type = self.packet_type,
                                                                secondary_header_flag = self.secondary_header_flag,
                                                                AP_ID = self.AP_ID,
                                                                sequence_flags = self.sequence_flags,
                                                                packet_sequence_count_or_name = count_or_name,
                                                                data_length = self.data_length))).tolist()

        finalPacket = numpy.append(finalHeader, packet)
        finalPacket = array.array('B', finalPacket[:])
        finalPacket = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(finalPacket), finalPacket))
        self.message_port_pub(pmt.intern('out'), finalPacket)

