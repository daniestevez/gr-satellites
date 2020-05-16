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

class telecommand_parser(gr.basic_block):
    """
    docstring for block CCSDS telemetry_parser
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="telecommand_parser",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytearray(pmt.u8vector_elements(msg))

        try:
            data = telecommand.FullPacket.parse(packet[:])
        except:
            print("Could not decode telecommand packet")
            return
        print(data)
