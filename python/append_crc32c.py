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
import pmt
import array
import struct

import crc32c

class append_crc32c(gr.basic_block):
    """
    docstring for block append_crc32c
    """
    def __init__(self, include_header):
        gr.basic_block.__init__(self,
            name="append_crc32c",
            in_sig=[],
            out_sig=[])

        self.include_header = include_header
        
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = array.array("B", pmt.u8vector_elements(msg))
        crc = crc32c.crc(packet if self.include_header else packet[4:])
        packet += array.array("B", struct.pack(">I", crc))
        self.message_port_pub(pmt.intern('out'),
                              pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet)))
