#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import threading

import pmt
from gnuradio import gr
import zmq


class csp_zmq_sub(gr.sync_block):
    """CSP ZMQ SUB block"""
    def __init__(self, address, destinations):
        gr.sync_block.__init__(
            self,
            name='csp_zmq_sub',
            in_sig=[],
            out_sig=[]
        )

        ctx = zmq.Context()
        self.socket = ctx.socket(zmq.SUB)
        self.socket.connect(address)
        for dest in destinations:
            self.socket.setsockopt(zmq.SUBSCRIBE, bytes([dest]))

        self.message_port_register_out(pmt.intern('out'))

        self.run_thread = threading.Thread(target=self.run, daemon=True)
        self.run_thread.start()

    def run(self):
        while True:
            msg = self.socket.recv()
            if len(msg) < 5:
                print('[csp_zmq_sub] message too short; dropping')
            # strip out destination
            msg = msg[1:]
            # byte-swap CSP header, since CSP ZMQ uses CSP headers in opposite
            # endianness compared to over-the-air
            msg = msg[:4][::-1] + msg[4:]
            msg = pmt.cons(pmt.PMT_NIL,
                           pmt.init_u8vector(len(msg), list(msg)))
            self.message_port_pub(pmt.intern('out'), msg)
