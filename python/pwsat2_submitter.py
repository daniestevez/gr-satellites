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

# This contains code taken from https://github.com/PW-Sat2/SimpleUploader-radio.pw-sat.pl

import numpy
from gnuradio import gr
import pmt

from . import hdlc

import json
import base64
import datetime

class pwsat2_submitter(gr.basic_block):
    """
    docstring for block pwsat2_submitter
    """
    def __init__(self, credentials_file, initialTimestamp):
        gr.basic_block.__init__(self,
            name="pwsat2_submitter",
            in_sig=[],
            out_sig=[])
        self.requests = __import__('requests')
        
        self.baseUrl = 'http://radio.pw-sat.pl'
        self.headers = {'content-type': 'application/json'}

        dtformat = '%Y-%m-%d %H:%M:%S'
        self.initialTimestamp = datetime.datetime.strptime(initialTimestamp, dtformat) \
            if initialTimestamp != '' else None
        self.startTimestamp = datetime.datetime.utcnow()

        self.authenticate(credentials_file)
        
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def authenticate(self, credentials_path):
        try:
            credentials = self.loadCredentials(credentials_path)
        except (ValueError, IOError) as e:
            print('Could not load credentials for', self.baseUrl)
            print(e)
            self.cookies = None
            return

        url = self.baseUrl+'/api/authenticate'
        response = self.requests.post(url, data=json.dumps(credentials), headers=self.headers)
        if response.status_code == 200:
            self.cookies = response.cookies
        else:
            print('Could not authenticate to PW-Sat2 server')
            print('Reply:', response.text)
            print('HTTP code', response.status_code)
            self.cookies = None
    
    def loadCredentials(self, path):
        with open(path) as f:
            credentials = json.load(f)
        return credentials

    def putPacket(self, frame, timestamp):
        if self.cookies is None:
            print('Not uploading packet to', self.baseUrl, 'as we are not authenticated')
            return
        url = self.baseUrl+'/communication/frame'

        payload = { 'frame': str(base64.b64encode(frame), encoding = 'ascii'),
                    'timestamp': int((timestamp - datetime.datetime(1970, 1, 1)).total_seconds() * 1000),
                    'traffic': 'Rx'}

        response = self.requests.put(url, data=json.dumps(payload), headers=self.headers, cookies=self.cookies)
        return response.text
    
    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return

        data = bytearray(pmt.u8vector_elements(msg))
        crc = hdlc.crc_ccitt(data)
        data.append(crc & 0xff)
        data.append((crc >> 8) & 0xff)

        frame = bytes(data)
        
        now = datetime.datetime.utcnow()
        timestamp = now - self.startTimestamp + self.initialTimestamp \
          if self.initialTimestamp else now

        response = self.putPacket(frame, timestamp)
        if response:
            print('Packet uploaded to', self.baseUrl, response)
