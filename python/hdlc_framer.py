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

from . import hdlc

class hdlc_framer(gr.basic_block):
    """
    docstring for block hdlc_framer
    """
    def __init__(self, preamble_bytes, postamble_bytes):
        gr.basic_block.__init__(self,
            name="hdlc_framer",
            in_sig=None,
            out_sig=None)

        self.preamble_bytes = preamble_bytes
        self.postamble_bytes = postamble_bytes
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return

        data = list(pmt.u8vector_elements(msg))
        crc = hdlc.crc_ccitt(data)
        data.append(crc & 0xff)
        data.append((crc >> 8) & 0xff)
                
        buff = hdlc.flag * self.preamble_bytes
        ones = 0 # number of consecutive ones
        for byte in data:
            for _ in range(8):
                # transmit byte LSB first
                x = byte & 1
                buff.append(x)
                if x:
                    ones += 1
                else:
                    ones = 0
                if ones == 5:
                    # bit-stuff
                    buff.append(0)
                    ones = 0
                byte >>= 1
        buff.extend(hdlc.flag * self.postamble_bytes)

        self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(buff), buff)))
