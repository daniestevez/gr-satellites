#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import numpy
import pmt


class snet_classifier(gr.basic_block):
    """docstring for block snet_classifier"""
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='snet_classifier',
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('SNET-A'))
        self.message_port_register_out(pmt.intern('SNET-B'))
        self.message_port_register_out(pmt.intern('SNET-C'))
        self.message_port_register_out(pmt.intern('SNET-D'))

    def handle_msg(self, msg_pmt):
        srcId = pmt.dict_ref(pmt.car(msg_pmt),
                             pmt.intern('SNET SrcId'), pmt.PMT_NIL)
        if pmt.eq(srcId, pmt.PMT_NIL):
            return
        sat = pmt.to_long(srcId) >> 1

        if sat == 0:
            satellite = 'SNET-A'
        elif sat == 1:
            satellite = 'SNET-B'
        elif sat == 2:
            satellite = 'SNET-C'
        elif sat == 3:
            satellite = 'SNET-D'
        else:
            return

        self.message_port_pub(pmt.intern(satellite), msg_pmt)
