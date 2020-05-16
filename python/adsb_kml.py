#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2016 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
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

