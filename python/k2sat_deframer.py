#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Daniel Estevez <daniel@destevez.net>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

import numpy
from gnuradio import gr
import pmt
import array
from . import hdlc_deframer
from . import hdlc
import binascii

class k2sat_deframer(gr.basic_block):
    """
    docstring for block k2sat_deframer
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="k2sat_deframer",
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
        data = array.array('B', [0x7e]) + packet # add 0x7e HDLC flag for CRC-16 check
        checksum = 0xFFFF
        for d in data:
            checksum = ((checksum << 8) & 0xFF00) ^ self.crc_table[((checksum >> 8) ^ d) & 0x00FF]
        return checksum == 0
        
    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = array.array("B", pmt.u8vector_elements(msg))

        # search all packet end markers in current packet
        start = 0
        while True:
            idx = packet[start:].tostring().find('\x7e\x55\x55\x55') # find packet end marker
            if idx == -1:
                break
            if self.check_packet(packet[:idx]): # check if this is a valid packet
                ax25_packet = packet[:-2+idx]
                self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(ax25_packet), ax25_packet)))
            start = idx + 2

        return

