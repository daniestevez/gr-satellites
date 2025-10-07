#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# This contains code taken from
# https://github.com/PW-Sat2/SimpleUploader-radio.pw-sat.pl
# That code is licenced under the following terms:

# MIT License
#
# Copyright (c) 2017 SoftwareMill
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import base64
import datetime
import json

from gnuradio import gr
import numpy
import pmt

from . import crc, hdlc
from .submit import parse_timestamp


class pwsat2_submitter(gr.basic_block):
    """docstring for block pwsat2_submitter"""
    def __init__(self, credentials_file, initialTimestamp):
        gr.basic_block.__init__(
            self,
            name="pwsat2_submitter",
            in_sig=[],
            out_sig=[])
        self.crc_calc = crc(16, 0x1021, 0xFFFF, 0xFFFF, True, True)
        self.requests = __import__('requests')

        self.baseUrl = 'http://radio.pw-sat.pl'
        self.headers = {'content-type': 'application/json'}

        self.initialTimestamp = (
            parse_timestamp(initialTimestamp)
            if initialTimestamp != '' else None)
        self.startTimestamp = datetime.datetime.now(datetime.timezone.utc)

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
        response = self.requests.post(url,
                                      data=json.dumps(credentials),
                                      headers=self.headers)
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
            print('Not uploading packet to',
                  self.baseUrl,
                  'as we are not authenticated')
            return
        url = self.baseUrl+'/communication/frame'

        timestamp = int(timestamp.timestamp() * 1e3)
        payload = {'frame': str(base64.b64encode(frame), encoding='ascii'),
                   'timestamp': timestamp,
                   'traffic': 'Rx'}

        response = self.requests.put(url,
                                     data=json.dumps(payload),
                                     headers=self.headers,
                                     cookies=self.cookies)
        return response.text

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return

        data = list(pmt.u8vector_elements(msg))
        crc_val = self.crc_calc.compute(data)
        data.append(crc_val & 0xff)
        data.append((crc_val >> 8) & 0xff)

        frame = bytes(data)

        now = datetime.datetime.now(datetime.timezone.utc)
        timestamp = (now - self.startTimestamp + self.initialTimestamp
                     if self.initialTimestamp else now)

        response = self.putPacket(frame, timestamp)
        if response:
            print('Packet uploaded to', self.baseUrl, response)
