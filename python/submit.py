#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy
from gnuradio import gr
import pmt
import datetime
import urllib.request, urllib.parse, urllib.error

class submit(gr.basic_block):
    """
    docstring for block submit
    """
    def __init__(self, url, noradID, source, longitude, latitude, initialTimestamp):
        gr.basic_block.__init__(self,
            name="submit",
            in_sig=[],
            out_sig=[])

        self.url = url
        self.request = { 'noradID': noradID,\
                         'source': source,\
                         'locator': 'longLat',\
                         'longitude': str(abs(longitude)) + ('E' if longitude >= 0 else 'W'),\
                         'latitude': str(abs(latitude)) + ('N' if latitude >= 0 else 'S'),\
                         'version': '1.6.6' }
        dtformat = '%Y-%m-%d %H:%M:%S'
        self.initialTimestamp = datetime.datetime.strptime(initialTimestamp, dtformat) \
            if initialTimestamp != '' else None
        self.startTimestamp = datetime.datetime.utcnow()
        
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        

    def handle_msg(self, msg_pmt):
        # check that callsign and QTH have been entered
        if self.request['source'] == '':
            return
        if self.request['longitude'] == 0.0 and self.request['latitude'] == 0.0:
            return

        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return

        self.request['frame'] = bytes(pmt.u8vector_elements(msg)).hex().upper()
        
        now = datetime.datetime.utcnow()
        timestamp = now - self.startTimestamp + self.initialTimestamp \
          if self.initialTimestamp else now
        self.request['timestamp'] = timestamp.isoformat()[:-3] + 'Z'

        params = bytes(urllib.parse.urlencode(self.request), encoding = 'ascii')
        try:
            f = urllib.request.urlopen('{}?{}'.format(self.url, params), data=params)
        except Exception as e:
            print('Error while submitting telemetry:', e)
            return
        reply = f.read()
        code = f.getcode()
        if code < 200 or code >= 300:
            print("Server error while submitting telemetry")
            print("Reply:")
            print(reply)
            print("URL:", f.geturl())
            print("HTTP code:", f.getcode())
            print("Info:")
            print(f.info())
        f.close()
        
