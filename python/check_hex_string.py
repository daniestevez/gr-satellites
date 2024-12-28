#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 DL7NDR Daniel (https://www.qrz.com/db/DL7NDR)
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from gnuradio import gr
import pmt


class check_hex_string(gr.basic_block):
    """docstring for block check_hex_string"""
    def __init__(self, hexstring, startindex=0):
        gr.basic_block.__init__(
            self,
            name='check_hex_string',
            in_sig=[],
            out_sig=[])

        self.hexstring = bytes.fromhex(hexstring)
        self.startindex = startindex

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

        # Check packet length
        if len(packet) < len(self.hexstring):
            self.message_port_pub(pmt.intern('fail'), msg_pmt)
            return

        hex_str = packet[self.startindex:self.startindex + len(self.hexstring)]

        if (hex_str == self.hexstring):
            # match
            self.message_port_pub(pmt.intern('ok'), msg_pmt)
        else:
            # no match
            self.message_port_pub(pmt.intern('fail'), msg_pmt)
