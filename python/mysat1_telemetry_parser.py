#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Daniel Estevez <daniel@destevez.net>
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

import mysat1_telemetry

class mysat1_telemetry_parser(gr.basic_block):
    """
    docstring for block mysat1_telemetry_parser
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="mysat1_telemetry_parser",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        # print (msg)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = bytearray(pmt.u8vector_elements(msg))

        try:
            data = mysat1_telemetry.Beacon.parse(packet[16:])
        except:
            print "Could not decode telemetry beacon"
            return
        data.obc_temp.obc_temp -= 128
        data.obc_temp.obc_daughter_board_temp -= 128
        data.eps_temp.eps_board_temp -= 128
        data.eps_temp.eps_battery_temp -= 128
        data.ants.ants_temp -= 128
        data.trxvu_temp.trxvu_temp -= 128
        data.adcs.adcs_temp -= 128
        for i in range(len(data.solar_panels.solar_panels_temp)):
            data.solar_panels.solar_panels_temp[i] -= 128
        data.obc_voltages.obc_3v3_voltage /= 10.0
        data.obc_voltages.obc_5v0_voltage /= 10.0
        data.eps_batt_voltage.eps_batt_voltage /= 10.0
        data.trxvu_voltage.trxvu_voltage /= 10.0
        print(data)
        