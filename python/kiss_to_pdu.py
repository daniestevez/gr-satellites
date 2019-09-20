#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 Daniel Estevez <daniel@destevez.net>.
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

import numpy
from gnuradio import gr
import collections
import pmt
import array

from .kiss import *

class kiss_to_pdu(gr.sync_block):
    """
    docstring for block kiss_to_pdu
    """
    def __init__(self, control_byte=True):
        gr.sync_block.__init__(self,
            name="kiss_to_pdu",
            in_sig=[numpy.uint8],
            out_sig=[])

        self.kiss = collections.deque()
        self.pdu = list()
        self.transpose = False
        self.control_byte = control_byte

        self.message_port_register_out(pmt.intern('out'))

    def work(self, input_items, output_items):
        self.kiss.extend(input_items[0])
        
        while self.kiss:
            c = self.kiss.popleft()
            if c == FEND:
                if self.pdu and (not self.control_byte or not self.pdu[0] & 0x0f):
                    msg = array.array('B', self.pdu[1:] if self.control_byte else self.pdu)
                    self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(msg), msg)))
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

