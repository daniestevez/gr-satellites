#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 

import numpy
from gnuradio import gr
import pmt

import traceback

from . import dstar_one_telemetry

class dstar_one_telemetry_parser(gr.basic_block):
    """
    docstring for block dstar_one_telemetry_parser
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="dstar_one_telemetry_parser",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytes(pmt.u8vector_elements(msg))

        try:
            data = dstar_one_telemetry.Beacon.parse(packet[2:])
        except Exception:
            print("Could not decode telemetry beacon")
            traceback.print_exc()
            return
        print(data)
