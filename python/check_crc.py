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
import csp_header

class check_crc(gr.basic_block):
    """
    docstring for block check_crc
    """
    def __init__(self, include_header, verbose, force=False):
        gr.basic_block.__init__(self,
            name="check_crc",
            in_sig=[],
            out_sig=[])

        self.include_header = include_header
        self.verbose = verbose
        self.force = force
        
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('ok'))
        self.message_port_register_out(pmt.intern('fail'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = array.array("B", pmt.u8vector_elements(msg))
        try:
            header = csp_header.CSP(packet[:4])
        except ValueError as e:
            if self.verbose:
                print e
            return
        if not self.force and not header.crc:
            if self.verbose:
                print "CRC not used"
            self.message_port_pub(pmt.intern('ok'), msg_pmt)
        else:
            if len(packet) < 8: # bytes CSP header, 4 bytes CRC-32C
                if self.verbose:
                    print "Malformed CSP packet (too short)"
                return
            crc = crc32c.crc(packet[:-4] if self.include_header else packet[4:-4])
            packet_crc = struct.unpack(">I", packet[-4:])[0]
            if crc == packet_crc:
                if self.verbose:
                    print "CRC OK"
                self.message_port_pub(pmt.intern('ok'), msg_pmt)
            else:
                if self.verbose:
                    print "CRC failed"
                self.message_port_pub(pmt.intern('fail'), msg_pmt)
