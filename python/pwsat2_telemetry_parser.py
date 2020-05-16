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

import pprint

class pwsat2_telemetry_parser(gr.basic_block):
    """
    docstring for block pwsat2_telemetry_parser
    """
    def __init__(self, pwsat2_path):
        gr.basic_block.__init__(self,
            name="pwsat2_telemetry_parser",
            in_sig=[],
            out_sig=[])

        import sys
        import pprint

        sys.path.append(pwsat2_path)
        sys.path.append(pwsat2_path + '/PWSat2OBC/integration_tests/')

        self.pwsat2_decoder = __import__('payload_decoder')

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytes(pmt.u8vector_elements(msg))

        try:
            data = self.pwsat2_decoder.PayloadDecoder.decode(packet[16:])
        except Exception as e:
            print("Could not decode telemetry beacon")
            print(e)
            return
        pprint.pprint(data)
