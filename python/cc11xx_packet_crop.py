#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import numpy
import pmt


class cc11xx_packet_crop(gr.basic_block):
    """docstring for block cc11xx_packet_crop"""
    def __init__(self, use_crc16):
        gr.basic_block.__init__(
            self,
            name='cc11xx_packet_handler',
            in_sig=[],
            out_sig=[])

        self.crc16 = use_crc16

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))

        crc_len = 2 if self.crc16 else 0
        packet_length = packet[0] + 1 + crc_len

        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.car(msg_pmt),
                     pmt.init_u8vector(packet_length, packet)))
