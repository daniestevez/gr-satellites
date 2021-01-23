#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import pmt

from .ao40_uncoded_crc import crc

class check_ao40_uncoded_crc(gr.basic_block):
    """
    docstring for block check_ao40_uncoded_crc
    """
    def __init__(self, verbose):
        gr.basic_block.__init__(self,
            name="check_ao40_uncoded_crc",
            in_sig=[],
            out_sig=[])

        self.verbose = verbose
        
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('ok'))
        self.message_port_register_out(pmt.intern('fail'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = pmt.u8vector_elements(msg)
        if crc(packet) == 0:
            if self.verbose:
                print("CRC OK")
            self.message_port_pub(pmt.intern('ok'), msg_pmt)
        else:
            if self.verbose:
                print("CRC failed")
            self.message_port_pub(pmt.intern('fail'), msg_pmt)
