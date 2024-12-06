#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import struct

from gnuradio import gr
import numpy
import pmt


class check_address2(gr.basic_block):
    """docstring for block check_address2"""
    def __init__(self, address):
        gr.basic_block.__init__(
            self,
            name='check_address2',
            in_sig=[],
            out_sig=[])

        self.callsign = address

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('ok'))
        self.message_port_register_out(pmt.intern('fail'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))

        callsign = None

        # Check packet length
        if len(packet) < len(self.callsign):
            self.message_port_pub(pmt.intern('fail'), msg_pmt)
            return

        callsign = packet[:len(self.callsign)]

        try:
            callsign = bytes(callsign).decode('ascii').rstrip(' ')

        except UnicodeDecodeError:
            print("Not to ASCII convertable string detected.")

        if (callsign == self.callsign):
            # match
            self.message_port_pub(pmt.intern('ok'), msg_pmt)
        else:
            # no match
            self.message_port_pub(pmt.intern('fail'), msg_pmt)
