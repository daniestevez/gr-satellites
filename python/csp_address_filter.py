#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import pmt
from gnuradio import gr


class csp_address_filter(gr.sync_block):
    """CSP Address Filter block"""
    def __init__(self, allowed_sources, allowed_destinations):
        gr.sync_block.__init__(
            self,
            name='csp_address_filter',
            in_sig=[],
            out_sig=[]
        )
        self.sources = allowed_sources
        self.destinations = allowed_destinations
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] received invalid message type. Expected u8vector')
            return
        msg = pmt.u8vector_elements(msg)
        if len(msg) < 4:
            print('[csp_address_filter] message is too short')
            return
        # extract addresses from CSP header
        source = (msg[0] >> 1) & 0x1f
        destination = ((msg[0] & 1) << 4) | (msg[1] >> 4)
        if source not in self.sources or destination not in self.destinations:
            # drop packet
            return
        self.message_port_pub(pmt.intern('out'), msg_pmt)
