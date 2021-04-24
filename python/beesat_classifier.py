#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2016 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import struct

from gnuradio import gr
import numpy
import pmt


class beesat_classifier(gr.basic_block):
    """docstring for block beesat_classifier"""
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='beesat_classifier',
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('BEESAT-1'))
        self.message_port_register_out(pmt.intern('BEESAT-2'))
        self.message_port_register_out(pmt.intern('BEESAT-4'))
        self.message_port_register_out(pmt.intern('BEESAT-9'))
        self.message_port_register_out(pmt.intern('TECHNOSAT'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))
        satellite = None
        if len(packet) < 2 + 6 + 2:
            # 2byte header, 6byte callsign, 2byte callsign crc
            return
        callsign = struct.unpack('6s', packet[2:8])[0]
        if callsign == 'DP0BEE':
            satellite = 'BEESAT-1'
        elif callsign == 'DP0BEF':
            satellite = 'BEESAT-2'
        elif callsign == 'DP0BEH':
            satellite = 'BEESAT-4'
        elif callsign == 'DP0BEM':
            satellite = 'BEESAT-9'
        elif callsign == 'DP0TBA':
            satellite = 'TECHNOSAT'

        if satellite:
            self.message_port_pub(pmt.intern(satellite), msg_pmt)
