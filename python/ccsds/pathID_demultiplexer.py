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

class pathID_demultiplexer(gr.basic_block):
    """
    docstring for block pathID_demultiplexer
    """
    def __init__(self, pathID_outputs):
        gr.basic_block.__init__(self,
            name="pathID_demultiplexer",
            in_sig=[],
            out_sig=[])
        self.pathID_outputs = pathID_outputs
        self.message_port_register_in(pmt.intern('in'))

        self.outputDict = {}
        for i in range(len(pathID_outputs)):
            self.outputDict[pathID_outputs[i]] = i
            self.message_port_register_out(pmt.intern('out'+str(i)))

        self.message_port_register_out(pmt.intern('discarded'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytearray(pmt.u8vector_elements(msg))

        try:
            data = space_packet.PrimaryHeader.parse(packet[:])
        except:
            print("Could not decode space packet primary header")
            return

        outPort = data.AP_ID
        try:
            port = self.outputDict[outPort]
        except KeyError:
            self.message_port_pub(pmt.intern('discarded'), msg_pmt)
            print("Discarded message")
        else:
            self.message_port_pub(pmt.intern('out' + str(port)), msg_pmt)

