#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Daniel Estevez <daniel@destevez.net>.
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

class aausat4_remove_fsm(gr.basic_block):
    """
    docstring for block aausat4_remove_fsm
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="aausat4_remove_fsm",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('short'))
        self.message_port_register_out(pmt.intern('long'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_f32vector(msg):
            print("[ERROR] Received invalid message type. Expected f32vector")
            return
        packet_short = pmt.f32vector_elements(msg)[8:8+1020]
        packet_long = pmt.f32vector_elements(msg)[8:8+1996]
        self.message_port_pub(pmt.intern('short'),
                              pmt.cons(pmt.PMT_NIL, pmt.init_f32vector(len(packet_short), packet_short)))
        self.message_port_pub(pmt.intern('long'),
                              pmt.cons(pmt.PMT_NIL, pmt.init_f32vector(len(packet_long), packet_long)))
