#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 Daniel Estevez <daniel@destevez.net>
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

from csp_header import CSP

import numpy
from gnuradio import gr
import pmt

flags = {-1 : 'FLAG_CAM_ERR_POWERON',\
         -2 : 'FLAG_CAM_ERR_BEGIN',\
         -3 : 'FLAG_CAM_ERR_STOP',\
         -4 : 'FLAG_CAM_ERR_GETLEN',\
         -5 : 'FLAG_CAM_ERR_READ',\
         -6 : 'FLAG_FRAM_ERR_READ'}


class by701_image_decoder(gr.basic_block):
    """
    docstring for block by701_image_decoder
    """
    def __init__(self, path='/tmp', display=False):
        gr.basic_block.__init__(self,
            name="by701_image_decoder",
            in_sig=[],
            out_sig=[])

        self.path = path
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.files = dict()
        self.remaining = dict()
        self.display = display
        self.displaying = list()
                
    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = bytearray(pmt.u8vector_elements(msg))

        # check packet len
        if len(packet) <= 15+8:
            return
        
        csp = CSP(packet[:4])

        # destination 6 is used for JPEG chunks
        if csp.destination != 6:
            return

        image_id = struct.unpack('<I', packet[4:8])[0]
        flag = struct.unpack('<b', packet[8:9])[0]
        length = struct.unpack('<I', packet[9:12] + bytearray([0]))[0]
        index = struct.unpack('<I', packet[12:15] + bytearray([0]))[0]
        data = packet[15:-8]

        if flag in flags:
            print 'Received flag', flags[flag]
            return

        filename = os.path.join(self.path, str(image_id) + '.jpg')
        if image_id not in self.files:
            self.files[image_id] = open(filename, 'wb', 0)
            self.remaining[image_id] = length

        # check that index and length make sense
        if index + len(data) > length:
            return
            
        f = self.files[image_id]
        f.seek(index)
        f.write(data)

        self.remaining[image_id] = self.remaining[image_id] - len(data)

        if self.display and image_id not in self.displaying and \
          length - self.remaining[image_id] >= 64*10:
            self.displaying.append(image_id)
            try:
                subprocess.Popen(['feh', '-F', '-R', '1', filename])
            except Exception:
                pass
        
        if self.remaining[image_id] <= 0:
            # image finished
            print 'Finished downloading image', image_id
            f.close()
            del self.remaining[image_id]
            del self.files[image_id]
