#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Daniel Estevez <daniel@destevez.net>.
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

from .hdlc_deframer import fcs_ok

class check_astrocast_crc(gr.basic_block):
    """
    docstring for block check_astrocast_crc
    """
    def __init__(self, verbose):
        gr.basic_block.__init__(self,
            name="check_eseo_crc",
            in_sig=[],
            out_sig=[])

        self.verbose = verbose
        
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('ok'))
        self.message_port_register_out(pmt.intern('fail'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = array.array("B", pmt.u8vector_elements(msg))[1:] # drop initial 0x7e

        # find final 0x7e
        idx = packet.tostring().find('\x7e')
        if idx == -1:
            return
        
        packet_out = packet[:idx-2]
        msg_out = pmt.cons(pmt.car(msg_pmt), pmt.init_u8vector(len(packet_out), packet_out))
        if fcs_ok(packet[:idx]):
            if self.verbose:
                print("CRC OK")
            self.message_port_pub(pmt.intern('ok'), msg_out)
        else:
            if self.verbose:
                print("CRC failed")
            self.message_port_pub(pmt.intern('fail'), msg_out)
