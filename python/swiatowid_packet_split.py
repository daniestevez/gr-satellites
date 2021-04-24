#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import numpy
import pmt


class swiatowid_packet_split(gr.basic_block):
    """docstring for block swiatowid_packet_split"""
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='swiatowid_packet_split',
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
        packet = pmt.u8vector_elements(msg)

        for j in range(0, len(packet) - 2, 58):
            # -2 above is included for the case when the packet
            # carriers a CRC-16
            piece = packet[j:j+58]
            self.message_port_pub(
                pmt.intern('out'),
                pmt.cons(pmt.car(msg_pmt),
                         pmt.init_u8vector(len(piece), piece)))
