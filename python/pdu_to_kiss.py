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

from .kiss import *

class pdu_to_kiss(gr.basic_block):
    """
    docstring for block pdu_to_kiss
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="pdu_to_kiss",
            in_sig=None,
            out_sig=None)

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

