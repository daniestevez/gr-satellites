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
import numpy
import pmt


class check_address(gr.basic_block):
    """docstring for block check_address"""
    def __init__(self, address, direction, digicallsign):
        gr.basic_block.__init__(
            self,
            name='check_address',
            in_sig=[],
            out_sig=[])

        a = address.split('-')
        self.callsign = a[0]
        self.ssid = int(a[1]) if len(a) > 1 else None
        self.direction = direction
        self.digicallsign = digicallsign

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('ok'))
        self.message_port_register_out(pmt.intern('fail'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))

        # Check packet length.
        # An AX.25 header with 2 addresses, control and PID is 16 bytes.
        if len(packet) < 16:
            self.message_port_pub(pmt.intern('fail'), msg_pmt)
            return

        if self.direction == 'to':
            address = packet[:7]
        else:
            address = packet[7:14]

        hbit = 0
        if len(packet) > 20:

            hbit = packet[20] >> 7
# digi callsign; and above: hbit  (most significant bit after digi callsign)
# (set to 1 in case of digipeated message)
            digi = [c >> 1 for c in packet[14:20]]

            digi = bytes(digi).decode('ascii').rstrip(' ')

# extension bit (least significant bit after sender callsign)
# (set to 0 in case of digi callsign follows)
        ebit = packet[13] & 0x01

        callsign = [c >> 1 for c in address[:6]]

        callsign = bytes(callsign).decode('ascii').rstrip(' ')

        ssid = (address[6] >> 1) & 0x0f

# altered if sentence
        if ((callsign == self.callsign
                and (self.ssid is None or ssid == self.ssid))
                or (ebit == 0 and hbit == 1 and digi == self.digicallsign)):
            # match
            self.message_port_pub(pmt.intern('ok'), msg_pmt)
        else:
            # no match
            self.message_port_pub(pmt.intern('fail'), msg_pmt)
