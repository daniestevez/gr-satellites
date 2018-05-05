#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Daniel Estévez
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
# 

import numpy
from gnuradio import gr
import pmt
import array

class snet_classifier(gr.basic_block):
    """
    docstring for block snet_classifier
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="snet_classifier",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('SNET-A'))
        self.message_port_register_out(pmt.intern('SNET-B'))
        self.message_port_register_out(pmt.intern('SNET-C'))
        self.message_port_register_out(pmt.intern('SNET-D'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = array.array("B", pmt.u8vector_elements(msg))

        srcId = pmt.dict_ref(pmt.car(msg_pmt), pmt.intern('SNET SrcId'), pmt.PMT_NIL)
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
