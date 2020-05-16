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
from . import telemetry
import pmt

class virtual_channel_demultiplexer(gr.basic_block):
    """
    docstring for block virtual_channel_demultiplexer
    """
    def __init__(self, vc_outputs):
        gr.basic_block.__init__(self,
            name="virtual_channel_demultiplexer",
            in_sig=[],
            out_sig=[])

        self.vc_outputs = vc_outputs
        self.message_port_register_in(pmt.intern('in'))

        self.outputDict = {}
        for i in range(len(vc_outputs)):
            self.outputDict[vc_outputs[i]] = i
            self.message_port_register_out(pmt.intern('out' + str(i)))

        self.message_port_register_out(pmt.intern('discarded'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytearray(pmt.u8vector_elements(msg))

        try:
            data = telemetry.PrimaryHeader.parse(packet[:])
        except:
            print("Could not decode telemetry primary header")
            return

        outPort = data.virtual_channel_id
        try:
            port = self.outputDict[outPort]
        except KeyError:
            self.message_port_pub(pmt.intern('discarded'), msg_pmt)
            print("Discarded message")
        else:
            self.message_port_pub(pmt.intern('out' + str(port)), msg_pmt)
