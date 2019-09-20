#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Daniel Estevez <daniel@destevez.net>.
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
import struct

class check_address(gr.basic_block):
    """
    docstring for block check_address
    """
    def __init__(self, address, direction):
        gr.basic_block.__init__(self,
            name="check_address",
            in_sig=[],
            out_sig=[])

        a = address.split('-')
        self.callsign = a[0]
        self.ssid = int(a[1]) if len(a) > 1 else None
        self.direction = direction
        
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('ok'))
        self.message_port_register_out(pmt.intern('fail'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = array.array("B", pmt.u8vector_elements(msg))

        # check packet length
        # an AX.25 header with 2 addresses, control and PID is 16 bytes
        if len(packet) < 16:
            self.message_port_pub(pmt.intern('fail'), msg_pmt)
            return

        if self.direction == 'to':
            address = packet[:7]
        else:
            address = packet[7:14]

        callsign = array.array('B', [c >> 1 for c in address[:6]]).tostring().rstrip(' ')
        ssid = int((address[6] >> 1) & 0x0f)

        if callsign != self.callsign or (self.ssid != None and ssid != self.ssid):
            # incorrect address
            self.message_port_pub(pmt.intern('fail'), msg_pmt)
        else:
            # correct address
            self.message_port_pub(pmt.intern('ok'), msg_pmt)
