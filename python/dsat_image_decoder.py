#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 Daniel Estevez <daniel@destevez.net>
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
from datetime import datetime

from .csp_header import CSP
from .feh import FehOpener

import numpy
from gnuradio import gr
import pmt

class dsat_image_decoder(gr.basic_block):
    """
    docstring for block by701_image_decoder
    """
    def __init__(self, path='/tmp', display=False, fullscreen=True):
        gr.basic_block.__init__(self,
            name="dsat_image_decoder",
            in_sig=[],
            out_sig=[])

        self.path = path
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.files = dict()
        self.remaining = dict()
        self.display = display
        self.displaying = list()
        self.current_id = None
        self.feh = FehOpener(fullscreen)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytearray(pmt.u8vector_elements(msg))

        # check packet len
        if len(packet) <= 15+8:
            return
        
        csp = CSP(packet[:4])

        # destination port 12 is used for announcements
        if csp.dest_port == 12:
            self.current_timestamp = datetime.utcfromtimestamp(struct.unpack('<i', packet[4:8])[0])
            self.current_id = struct.unpack('<I', packet[8:12])[0]
            # next 12 bytes are for GPS position
            self.length = struct.unpack('<I', packet[21:25])[0]

            print('Image {} announced. Length {}. Timestamp {}'.format(self.current_id,
                                                                       self.length, self.current_timestamp))

            self.filename = os.path.join(self.path, str(self.current_id) + '.jpg')
            if self.current_id not in self.files:
                self.files[self.current_id] = open(self.filename, 'wb', 0)
                self.remaining[self.current_id] = self.length

            self.bytes_done = 0
            self.old_index = 0

            return

        # destination port 30 is used for JPEG blocks
        if csp.dest_port != 30:
            return

        if not self.current_id:
            # we haven't heard the image announcement, we have to ignore the block
            return

        data = packet[4:-8]
        index = struct.unpack('>I', packet[-8:-4])[0]

        # handle index rollover
        if self.old_index > index:
            self.bytes_done += self.msg_datasize
        self.old_index = index
        
        self.msg_datasize = struct.unpack('>I', packet[-4:])[0] # not really needed to decode image
            
        f = self.files[self.current_id]
        f.seek(self.bytes_done + index)
        f.write(data)

        self.remaining[self.current_id] = self.remaining[self.current_id] - len(data)

        if self.display and self.current_id not in self.displaying and \
          self.length - self.remaining[self.current_id] >= 64*10:
            self.displaying.append(self.current_id)
            try:
                self.feh.open(self.filename)
            except Exception:
                pass
        
        if self.remaining[self.current_id] <= 0:
            # image finished
            print('Finished downloading image', self.current_id)
            f.close()
            del self.remaining[self.current_id]
            del self.files[self.current_id]
