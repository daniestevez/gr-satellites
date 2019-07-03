#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Daniel Estevez <daniel@destevez.net>.
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
import datetime

class aprs2text(gr.basic_block):
    """
    docstring for block aprs2text
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="aprs2text",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = array.array("B", pmt.u8vector_elements(msg))

        timestamp = datetime.datetime.utcnow().strftime('%y/%m/%d:%H/%M/%S')
        address = packet[7:14]
        callsign = array.array('B', map(lambda c: c >> 1, address[:6])).tostring().rstrip(' ')
        ssid = int((address[6] >> 1) & 0x0f)
        callsign_text = callsign + '-' + str(ssid) if ssid else callsign

        # find packet payload
        packet_payload = None
        for j in range(7, len(packet)-2, 7):
            if packet[j-1] & 1:
                packet_payload = packet[j+2:]
                break
        if packet_payload is None:
            return

        msg_out = array.array('B', timestamp + ':' + callsign_text + ':') + packet_payload + array.array('B', '\n')
        
        self.message_port_pub(pmt.intern('out'),  pmt.cons(pmt.car(msg_pmt), pmt.init_u8vector(len(msg_out), msg_out)))
