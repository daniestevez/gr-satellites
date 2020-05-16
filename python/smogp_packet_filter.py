#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy
from gnuradio import gr
import pmt

class smogp_packet_filter(gr.basic_block):
    """
    Filters out SMOG-P or ATL-1 packets not having a valid packet type

    The packet type is stored in the first byte
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="smogp_packet_filter",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    _valid_packet_types = [1, 2, 3, 4, 5, 6, 7, 33, 34, 129, 130, 131]
        
    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytes(pmt.u8vector_elements(msg))
        packet_type = packet[0]

        if packet_type in self._valid_packet_types:
            self.message_port_pub(pmt.intern('out'), msg_pmt)
