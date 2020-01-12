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

from .telemetry import gomx_3 as tlm

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
        beacon = tlm.parse(packet)
        
        # check that message is beacon
        if beacon.csp_header.destination != 10 or beacon.csp_header.destination_port != 30:
            return

        if beacon.csp_header.source != 1 or beacon.beacon_type != 0:
            return

        adsb = beacon.beacon.adsb

        
        print("""<Placemark>
        <name>{}</name>
        <description>Altitude: {}ft Time: {}</description>
        <styleUrl>#plane</styleUrl>
        <Point><coordinates>{},{}</coordinates></Point>
</Placemark>""".format(hex(adsb.last_icao), adsb.last_alt,
                        adsb.last_time,
                        adsb.last_lon if adsb.last_lon <= 180 else adsb.last_lon - 360,
                        adsb.last_lat))

