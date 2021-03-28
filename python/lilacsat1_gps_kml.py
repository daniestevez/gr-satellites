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

from .telemetry import by70_1


class lilacsat1_gps_kml(gr.basic_block):
    """docstring for block lilacsat1_gps_kml"""
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='lilacsat1_gps_kml',
            in_sig=None,
            out_sig=None)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))

        if len(packet) <= 4+8:
            return

        frame = by70_1.parse(packet)

        # Destination 5 is used for telemetry
        if frame.csp_header.destination != 5:
            return

        data = by70_1.beacon

        if not data or 'latitude' not in data:
            return

        line = '{},{},{}\n'.format(data.longitude,
                                   data.latitude,
                                   data.altitude).encode('ascii')

        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(line), line)))
