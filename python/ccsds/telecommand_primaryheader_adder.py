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
from . import telecommand
import array

class telecommand_primaryheader_adder(gr.basic_block):
    """
    docstring for block telecommand_primaryheader_adder
    """
    def __init__(self, bypass, control, spacecraft_id, virtual_channel_id):
        gr.basic_block.__init__(self,
            name="telecommand_primaryheader_adder",
            in_sig=[],
            out_sig=[])

        ##################################################
        # Parameters
        ##################################################
        self.transfer_frame_version = 0
        self.bypass = bypass
        self.control = control
        self.RSVD_spare = 0
        self.spacecraft_id = spacecraft_id
        self.virtual_channel_id = virtual_channel_id
        self.frame_length = 0
        self.frame_sequence_number = 0

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
        self.frame_length = len(packet) + 5
        if self.bypass == 1:
            self.frame_sequence_number = 0
        else:
            self.frame_sequence_number += 1

        finalHeader = array.array('B', telecommand.PrimaryHeader.build(dict(transfer_frame_version = self.transfer_frame_version,
                                                                            bypass = self.bypass,
                                                                            control = self.control,
                                                                            RSVD_spare = self.RSVD_spare,
                                                                            spacecraft_id = self.spacecraft_id,
                                                                            virtual_channel_id = self.virtual_channel_id,
                                                                            frame_length = self.frame_length,
                                                                            frame_sequence_number = self.frame_sequence_number))).tolist()

        finalPacket = numpy.append(finalHeader, packet)
        finalPacket = array.array('B', finalPacket[:])
        finalPacket = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(finalPacket), finalPacket))
        self.message_port_pub(pmt.intern('out'), finalPacket)

