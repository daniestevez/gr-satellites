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

from .csp_header import CSP
from . import gomx3_beacon

class adsb_kml(gr.basic_block):
    """
    docstring for block adsb_kml
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="adsb_kml",
            in_sig=None,
            out_sig=None)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return

        packet = bytes(pmt.u8vector_elements(msg))
        header = CSP(packet[:4])
        # check that message is beacon
        if header.destination != 10 or header.dest_port != 30:
            return

        beacon_type = packet[4]
        payload = packet[4:]

        if header.source != 1 or beacon_type != 0 or len(payload) != 140:
            return

        beacon = gomx3_beacon.beacon_1_0(payload)

        
        print("""<Placemark>
        <name>{}</name>
        <description>Altitude: {}ft Time: {}</description>
        <styleUrl>#plane</styleUrl>
        <Point><coordinates>{},{}</coordinates></Point>
</Placemark>""".format(hex(beacon.adsb_last_icao), beacon.adsb_last_alt,
                        beacon.adsb_last_time,
                        beacon.adsb_last_lon if beacon.adsb_last_lon <= 180 else beacon.adsb_last_lon - 360,
                        beacon.adsb_last_lat))

