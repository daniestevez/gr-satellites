#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Daniel Estevez <daniel@destevez.net>
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

import struct
import os.path
import binascii
import subprocess

import numpy
from gnuradio import gr
import pmt

class sat_1kuns_pf_image_decoder(gr.basic_block):
    """
    docstring for block sat_1kuns_pf_image_decoder
    """
    def __init__(self, path='/tmp', display=False):
        gr.basic_block.__init__(self,
            name="sat_1kuns_pf_image_decoder",
            in_sig=[],
            out_sig=[])

        self.path = path
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.current_file = -1
        self.expected_block = 0
        self.display = display
        self.displaying = False
                
    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = bytearray(pmt.u8vector_elements(msg))

        # check packet len
        if len(packet) != 138:
            return

        block = struct.unpack('>H', packet[4:6])[0]
        data = packet[6:-4]

        if self.current_file == -1:
            if block == 0:
                # first file received
                print "Starting image 0"
                self.current_file = 0
                self.filename = os.path.join(self.path, 'img{}.jpg'.format(self.current_file))
                self.f = open(self.filename, 'wb', 0)
            else:
                return
        elif block == 0:
            # new file
            print "Image {} finished. Starting image {}".format(self.current_file, self.current_file+1)
            self.f.close()
            self.current_file += 1
            self.expected_block = 0
            self.filename = os.path.join(self.path, 'img{}.jpg'.format(self.current_file))
            self.f = open(self.filename, 'wb', 0)
            self.displaying = False
        elif block != self.expected_block:
            # lost block
            print "Lost image block {}".format(self.expected_block)
        
        print "Received image block {}".format(block)
        self.f.write(data)
        self.expected_block = block + 1

        if self.display and not self.displaying and block >= 5:
            self.displaying = True
            try:
                subprocess.Popen(['feh', '-F', '-R', '1', self.filename])
            except Exception:
                pass
