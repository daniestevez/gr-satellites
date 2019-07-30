#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Athanasios Theocharis <athatheoc@gmail.com>
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
import space_packet

class pathID_demultiplexer(gr.basic_block):
    """
    docstring for block pathID_demultiplexer
    """
    def __init__(self, num_output):
        gr.basic_block.__init__(self,
            name="pathID_demultiplexer",
            in_sig=[],
            out_sig=[])
        self.num_output = num_output
        self.message_port_register_in(pmt.intern('in'))

        for i in range(num_output):
            self.message_port_register_out(pmt.intern('out'+str(i)))

        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = bytearray(pmt.u8vector_elements(msg))

        try:
            data = space_packet.FullPacket.parse(packet[:])
        except:
            print "Could not decode space packet"
            return

        outPort = data.__getattr__('primary').search('AP_ID')
        self.message_port_pub(pmt.intern('out'+str(outPort)), msg_pmt)
