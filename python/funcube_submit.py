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
import binascii
import hashlib
import requests

class funcube_submit(gr.basic_block):
    """
    docstring for block funcube_submit
    """
    def __init__(self, url, site_id, auth_code):
        gr.basic_block.__init__(self,
            name="funcube_submit",
            in_sig=[],
            out_sig=[])

        self.base_url = url
        self.site_id = site_id
        self.auth_code = auth_code
        
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        
    def digest(self, hex_string):
        md5 = hashlib.md5()
        md5.update(hex_string)
        md5.update(':')
        md5.update(self.auth_code)
        return binascii.b2a_hex(md5.digest())
        
    def handle_msg(self, msg_pmt):
        if not self.base_url or not self.site_id or not self.auth_code:
            return

        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return

        frame = binascii.b2a_hex(str(bytearray(pmt.u8vector_elements(msg)))).upper()
        frame = ' '.join([frame[j:j+2] for j in range(0, len(frame), 2)]) # add space every two hex chars

        url = self.base_url + '/api/data/hex/' + self.site_id + '/?digest=' + self.digest(frame)
        r = requests.post(url, data = frame, headers = {'Content-Type' : 'application/text'})
        if r.status_code != 200:
            print 'FUNcube server error while submitting telemetry'
            print 'Reply:', r.text
            print 'HTTP code', r.status_code

