#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy
from gnuradio import gr
import collections
import pmt

from .kiss import *

class pdu_to_kiss(gr.basic_block):
    """
    docstring for block pdu_to_kiss
    """
    def __init__(self, control_byte = False):
        gr.basic_block.__init__(self,
            name="pdu_to_kiss",
            in_sig=None,
            out_sig=None)
        self.control_byte = control_byte

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return

        buff = list()
        buff.append(FEND)
        if self.control_byte:
            buff.append(numpy.uint8(0))
        for x in pmt.u8vector_elements(msg):
            if x == FESC:
                buff.append(FESC)
                buff.append(TFESC)
            elif x == FEND:
                buff.append(FESC)
                buff.append(TFEND)
            else:
                buff.append(numpy.uint8(x))
        buff.append(FEND)

        buff = bytes(buff)

        self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(buff), buff)))

