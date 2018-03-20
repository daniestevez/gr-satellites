#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 Daniel Estévez
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
# 

import numpy
from gnuradio import gr
import pmt
import array
import struct

class beesat_classifier(gr.basic_block):
    """
    docstring for block beesat_classifier
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="beesat_classifier",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('BEESAT-1'))
        self.message_port_register_out(pmt.intern('BEESAT-2'))
        self.message_port_register_out(pmt.intern('BEESAT-4'))
        self.message_port_register_out(pmt.intern('TECHNOSAT'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = array.array("B", pmt.u8vector_elements(msg))
        satellite = None
        if len(packet) < 2 + 6 + 2:  # 2byte header, 6byte callsign, 2byte callsign crc
            return
        callsign = struct.unpack("6s", packet[2:8])[0]
        if callsign == 'DP0BEE':
            satellite = 'BEESAT-1'
        elif callsign == 'DP0BEF':
            satellite = 'BEESAT-2'
        elif callsign == 'DP0BEH':
            satellite = 'BEESAT-4'
        elif callsign == 'DP0TBA':
            satellite = 'TECHNOSAT'

        if satellite:
            self.message_port_pub(pmt.intern(satellite), msg_pmt)
