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

from . import hdlc_deframer
from . import hdlc


class k2sat_deframer(gr.basic_block):
    """docstring for block k2sat_deframer"""
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='k2sat_deframer',
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))
        self.number = 0

        # CRC-16 table construction
        self.crc_table = list()
        for i in range(256):
            tmp = 0
            if i & 1:
                tmp ^= 0x1021
            if i & 2:
                tmp ^= 0x2042
            if i & 4:
                tmp ^= 0x4084
            if i & 8:
                tmp ^= 0x8108
            if i & 16:
                tmp ^= 0x1231
            if i & 32:
                tmp ^= 0x2462
            if i & 64:
                tmp ^= 0x48C4
            if i & 128:
                tmp ^= 0x9188
            self.crc_table.append(tmp)

    def check_packet(self, packet):
        data = b'\x7e' + packet  # add 0x7e HDLC flag for CRC-16 check
        checksum = 0xFFFF
        for d in data:
            checksum = (((checksum << 8) & 0xFF00)
                        ^ self.crc_table[((checksum >> 8) ^ d) & 0x00FF])
        return checksum == 0

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))

        # Search all packet end markers in current packet
        start = 0
        while True:
            # Find packet end marker
            idx = packet[start:].find(b'\x7e\x55\x55\x55')
            if idx == -1:
                break
            # Check if this is a valid packet
            if self.check_packet(packet[:idx]):
                ax25_packet = packet[:-2+idx]
                ax25_packet = list(packet)  # conversion to list for pybind11
                self.message_port_pub(
                    pmt.intern('out'),
                    pmt.cons(pmt.PMT_NIL,
                             pmt.init_u8vector(len(ax25_packet), ax25_packet)))
            start = idx + 2

        return
