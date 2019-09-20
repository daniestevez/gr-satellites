#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 Daniel Estevez <daniel@destevez.net>.
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

from .csp_header import CSP
from . import gomx3_beacon

class gomx3_beacon_parser(gr.basic_block):
    """
    docstring for block gomx3_beacon_parser
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="gomx3_beacon_parser",
            in_sig=None,
            out_sig=None)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return

        packet = array.array("B", pmt.u8vector_elements(msg))
        try:
            header = CSP(packet[:4])
        except ValueError as e:
            print(e)
            return
        # check that message is beacon
        if header.destination != 10 or header.dest_port != 30:
            print("Not a beacon: destination address {} port {}".format(header.destination,
                                                                        header.dest_port))
            print()
            return
        if len(packet) < 5:
            print("Malformed beacon (too short)")
            return
        beacon_type = packet[4]
        payload = packet[4:]

        beacon = None
        if header.source == 1 and beacon_type == 0 and len(payload) == 140:
            beacon = gomx3_beacon.beacon_1_0(payload)

        print((beacon if beacon else "Beacon type {} {}".format(header.source, beacon_type)))
        print()

