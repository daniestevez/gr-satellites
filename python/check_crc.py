#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import struct

from gnuradio import gr
import pmt

from . import crc as _crc_module
from . import csp_header

_crc_fn = _crc_module(32, 0x1EDC6F41, 0xFFFFFFFF, 0xFFFFFFFF, True, True)


class check_crc(gr.basic_block):
    """docstring for block check_crc"""
    def __init__(self, include_header, verbose, force=False):
        gr.basic_block.__init__(
            self,
            name='check_crc',
            in_sig=[],
            out_sig=[])

        self.include_header = include_header
        self.verbose = verbose
        self.force = force

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('ok'))
        self.message_port_register_out(pmt.intern('fail'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = pmt.u8vector_elements(msg)
        try:
            header = csp_header.CSP(packet[:4])
        except ValueError as e:
            if self.verbose:
                print(e)
            return
        if not self.force and not header.crc:
            if self.verbose:
                print('CRC not used')
            self.message_port_pub(pmt.intern('ok'), msg_pmt)
        else:
            if len(packet) < 8:  # 4 bytes CSP header, 4 bytes CRC-32C
                if self.verbose:
                    print('Malformed CSP packet (too short)')
                return
            crc = _crc_fn.compute(
                list(packet[:-4] if self.include_header else packet[4:-4]))
            packet_crc = struct.unpack('>I', bytes(packet[-4:]))[0]
            if crc == packet_crc:
                if self.verbose:
                    print('CRC OK')
                self.message_port_pub(pmt.intern('ok'), msg_pmt)
            else:
                if self.verbose:
                    print('CRC failed')
                self.message_port_pub(pmt.intern('fail'), msg_pmt)
