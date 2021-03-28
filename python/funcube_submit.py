#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import hashlib

from gnuradio import gr
import numpy
import pmt
import requests


class funcube_submit(gr.basic_block):
    """docstring for block funcube_submit"""
    def __init__(self, url, site_id, auth_code):
        gr.basic_block.__init__(
            self,
            name='funcube_submit',
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
        md5.update(b':')
        md5.update(bytes(self.auth_code, encoding='ascii'))
        return md5.digest().hex()

    def handle_msg(self, msg_pmt):
        if not self.base_url or not self.site_id or not self.auth_code:
            return

        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return

        frame = bytes(bytes(pmt.u8vector_elements(msg)).hex().upper(),
                      encoding='ascii')
        # Add a space every two hex chars
        frame = b' '.join([frame[j:j+2] for j in range(0, len(frame), 2)])

        url = (self.base_url + '/api/data/hex/'
               + self.site_id + '/?digest=' + self.digest(frame))
        r = requests.post(url, data=frame,
                          headers={'Content-Type': 'application/text'})
        if r.status_code != 200:
            print('FUNcube server error while submitting telemetry')
            print('Reply:', r.text)
            print('HTTP code', r.status_code)
