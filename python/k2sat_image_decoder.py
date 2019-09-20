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

from .feh import FehOpener

import numpy
from gnuradio import gr
import pmt

class k2sat_image_decoder(gr.basic_block):
    """
    docstring for block k2sat_image_decoder
    """
    def __init__(self, path='/tmp', display=False, fullscreen = True):
        gr.basic_block.__init__(self,
            name="k2sat_image_decoder",
            in_sig=[],
            out_sig=[])

        self.num_images = 0
        self.path = path
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.display = display
        self.next_frame_count = None
        self.feh = FehOpener(fullscreen, interval = 0.1)
                
    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytearray(pmt.u8vector_elements(msg))

        # check packet len
        if len(packet) <= 16+4+1:
            return

        virtual_channel_frame_count = packet[16 + 2]
        first_header_pointer = packet[16 + 3]

        if first_header_pointer == 0x00:
            # first packet in image
            filename = os.path.join(self.path, 'image_{}.jpg'.format(self.num_images))
            self.f = open(filename, 'wb')
            print('Started image', self.num_images)
            self.num_images += 1
            self.next_frame_count = virtual_channel_frame_count

        if self.next_frame_count == None:
            # current image has failed
            return
        
        if virtual_channel_frame_count != self.next_frame_count:
            print('Lost image packet. Image decoding failed.')
            self.next_frame_count = None
            self.f.close()
            return

        self.f.write(packet[20:-1])
        self.f.flush()
        self.next_frame_count = (self.next_frame_count + 1) % 256

        if self.display and first_header_pointer == 0x00:
            try:
                self.feh.open(filename)
            except Exception:
                pass
        
        if first_header_pointer == 0xff:
            # last packet in image
            self.f.close()
            self.next_frame_count = None
            print('Finished downloading image')
        
