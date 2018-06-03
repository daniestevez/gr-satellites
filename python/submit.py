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
import binascii
import datetime
import urllib

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
            print "[ERROR] Received invalid message type. Expected u8vector"
            return

        self.request['frame'] = \
          binascii.b2a_hex(str(bytearray(pmt.u8vector_elements(msg)))).upper()
        
        now = datetime.datetime.utcnow()
        timestamp = now - self.startTimestamp + self.initialTimestamp \
          if self.initialTimestamp else now
        self.request['timestamp'] = timestamp.isoformat()[:-3] + 'Z'

        params = urllib.urlencode(self.request)
        f = urllib.urlopen('{}?{}'.format(self.url, params), data=params)
        reply = f.read()
        code = f.getcode()
        if code < 200 or code >= 300:
            print "Server error while submitting telemetry"
            print "Reply:"
            print reply
            print "URL:", f.geturl()
            print "HTTP code:", f.getcode()
            print "Info:"
            print f.info()
        f.close()
        
