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
from . import telemetry

class telemetry_parser(gr.basic_block):
    """
    docstring for block CCSDS telemetry_parser
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="telemetry_parser",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytearray(pmt.u8vector_elements(msg))
        size = len(packet) - 6
        try:
            header = telemetry.PrimaryHeader.parse(packet[:])
            if header.ocf_flag == 1:
                size -= 4
            data = telemetry.FullPacket.parse(packet[:], size=size)
        except:
            print("Could not decode telemetry packet")
            return
        print(data)
        self.message_port_pub(pmt.intern('out'), msg_pmt)

