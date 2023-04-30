#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017,2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import datetime
import urllib.error
import urllib.parse
import urllib.request

from gnuradio import gr
import pmt
import numpy


def parse_time(time):
    try:
        return datetime.datetime.fromisoformat(time)
    except AttributeError:
        # Workaround for Python version <3.7, which doesn't have
        # fromisoformat()
        return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')


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
            parse_time(initialTimestamp)
            if initialTimestamp != '' else None)
        self.startTimestamp = datetime.datetime.utcnow()

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

        now = datetime.datetime.utcnow()
        timestamp = (
            now - self.startTimestamp + self.initialTimestamp
            if self.initialTimestamp else now)
        self.request['timestamp'] = timestamp.isoformat()[:-3] + 'Z'

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
