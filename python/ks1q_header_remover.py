#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2016 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import numpy
import pmt


class ks1q_header_remover(gr.basic_block):
    """docstring for block ks1q_header_remover"""
    def __init__(self, verbose):
        gr.basic_block.__init__(
            self,
            name='ks1q_header_remover',
            in_sig=[],
            out_sig=[])

        self.verbose = verbose
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))

        if len(packet) <= 3:
            return

        if self.verbose:
            print('Spacecraft ID', packet[:2].hex())
            if packet[2] == 0x50:
                print('CSP downlink, protocol version 0')
            else:
                print('Unknown packet type')

        data = packet[3:]
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(data), data)))
