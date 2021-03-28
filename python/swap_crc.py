#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import numpy
import pmt

from . import csp_header


class swap_crc(gr.basic_block):
    """docstring for block swap_crc"""
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='swap_crc',
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))
        try:
            header = csp_header.CSP(packet[:4])
        except ValueError as e:
            return
        if not header.crc:
            self.message_port_pub(pmt.intern('out'), msg_pmt)
        else:
            if len(packet) < 8:  # 4 bytes CSP header, 4 bytes CRC-32C
                # Malformed
                return
            crc = packet[-4:]
            packet = packet[:-4] + crc[::-1]
            msg_pmt = pmt.cons(pmt.PMT_NIL,
                               pmt.init_u8vector(len(packet), packet))
            self.message_port_pub(pmt.intern('out'), msg_pmt)
