#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017,2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import datetime
import sys
import urllib.error
import urllib.parse
import urllib.request

from gnuradio import gr
import pmt
import numpy


def parse_timestamp(s):
    if sys.version_info < (3, 11):
        # in Python 3.10, fromisoformat() does not accept
        # a trailing Z, and it can only parse millisecond
        # resolution. We remove any trailing Z, and parse
        # the fractional seconds separately
        s = s.rstrip('Z')
        s_int, s_frac = s.split('.')
        t_int = datetime.datetime.fromisoformat(s_int)
        t_frac = float(f'0.{s_frac}')
        # Truncate t_frac to integer microseconds to match
        # behaviour of fromisoformat() in newer Python version
        t = t_int + datetime.timedelta(
            microseconds=int(t_frac * 1000000))
    else:
        t = datetime.datetime.fromisoformat(s)
    t = t.replace(tzinfo=datetime.timezone.utc)
    return t


class submit(gr.basic_block):
    """docstring for block submit"""
    def __init__(self, url, noradID, source,
                 longitude, latitude, initialTimestamp):
        gr.basic_block.__init__(
            self,
            name='submit',
            in_sig=[],
            out_sig=[])

        self.url = url
        self.request = {
            'noradID': noradID,
            'source': source,
            'locator': 'longLat',
            'longitude': str(
                abs(longitude)) + ('E' if longitude >= 0 else 'W'),
            'latitude': str(
                abs(latitude)) + ('N' if latitude >= 0 else 'S'),
            'version': '1.6.6',
            }
        self.initialTimestamp = (
            parse_timestamp(initialTimestamp)
            if initialTimestamp != '' else None)
        self.startTimestamp = datetime.datetime.now(tz=datetime.timezone.utc)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        # Check that callsign and QTH have been entered
        if self.request['source'] == '':
            return
        if (self.request['longitude'] == 0.0
                and self.request['latitude'] == 0.0):
            return

        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return

        self.request['frame'] = bytes(pmt.u8vector_elements(msg)).hex().upper()

        t_now = datetime.datetime.now(tz=datetime.timezone.utc)
        t_prop = (
            t_now - self.startTimestamp + self.initialTimestamp
            if self.initialTimestamp else t_now)
        t_prop_fmt = t_prop.replace(tzinfo=None).isoformat()[:-3] + 'Z'
        self.request['timestamp'] = t_prop_fmt

        params = urllib.parse.urlencode(self.request)
        try:
            f = urllib.request.urlopen(
                '{}?{}'.format(self.url, params),
                data=bytes(params, encoding='ascii'))
        except Exception as e:
            print('Error while submitting telemetry:', e)
            return
        reply = f.read()
        code = f.getcode()
        if code < 200 or code >= 300:
            print('Server error while submitting telemetry')
            print('Reply:')
            print(reply)
            print('URL:', f.geturl())
            print('HTTP code:', f.getcode())
            print('Info:')
            print(f.info())
        f.close()
