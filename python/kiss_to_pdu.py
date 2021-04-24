#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import collections

from gnuradio import gr
import numpy
import pmt

from .kiss import *


class kiss_to_pdu(gr.sync_block):
    """docstring for block kiss_to_pdu"""
    def __init__(self, control_byte=True):
        gr.sync_block.__init__(
            self,
            name='kiss_to_pdu',
            in_sig=[numpy.uint8],
            out_sig=[])

        self.pdu = list()
        self.transpose = False
        self.control_byte = control_byte

        self.message_port_register_out(pmt.intern('out'))

    def work(self, input_items, output_items):
        for c in input_items[0]:
            if c == FEND:
                if (self.pdu
                        and (not self.control_byte or not self.pdu[0] & 0x0f)):
                    msg = self.pdu[1:] if self.control_byte else self.pdu
                    self.message_port_pub(
                        pmt.intern('out'),
                        pmt.cons(pmt.PMT_NIL,
                                 pmt.init_u8vector(len(msg), msg)))
                self.pdu = list()
            elif self.transpose:
                if c == TFEND:
                    self.pdu.append(FEND)
                elif c == TFESC:
                    self.pdu.append(FESC)
                self.transpose = False
            elif c == FESC:
                self.transpose = True
            else:
                self.pdu.append(c)

        return len(input_items[0])
