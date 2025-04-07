#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import pmt
from gnuradio import gr
import zmq


class csp_zmq_pub(gr.sync_block):
    """CSP ZMQ PUB block"""
    def __init__(self, address):
        gr.sync_block.__init__(
            self,
            name='csp_zmq_pub',
            in_sig=[],
            out_sig=[]
        )

        ctx = zmq.Context()
        self.socket = ctx.socket(zmq.PUB)
        self.socket.connect(address)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] received invalid message type. Expected u8vector')
            return
        msg = bytes(pmt.u8vector_elements(msg))
        if len(msg) < 4:
            print('[csp_zmq_pub] message too short; dropping')
        csp_header = msg[:4]
        payload = msg[4:]
        # extract destination from CSP header
        dest = ((csp_header[0] & 1) << 4) | (csp_header[1] >> 4)
        # byte-swap csp_header, since CSP ZMQ uses headers in the opposite
        # endianness compared to over-the-air
        self.socket.send(bytes([dest]) + csp_header[::-1] + payload)
