#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017,2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy
from gnuradio import gr
import collections
import pmt
import datetime
import struct
import warnings

from .kiss import *
from .submit import parse_time

class pdu_to_kiss(gr.basic_block):
    """
    docstring for block pdu_to_kiss
    """
    def __init__(self, control_byte = True, include_timestamp = False,
                     initial_timestamp = ''):
        gr.basic_block.__init__(self,
            name="pdu_to_kiss",
            in_sig=None,
            out_sig=None)
        self.control_byte = control_byte
        self.include_timestamp = include_timestamp
        self.initial_timestamp = parse_time(initial_timestamp) \
            if initial_timestamp != '' else None
        self.start_timestamp = datetime.datetime.utcnow()

        if not control_byte and include_timestamp:
            warnings.warn('Using no control byte and timestamps in pdu_to_kiss will usually give problems')

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def create_timestamp(self):
        """Returns the timestamp as a KISS control frame with control byte 09

        The timestamp is the number of milliseconds elapsed since the UNIX
        epoch according to UTC and not counting leap seconds, stored as a
        big-endian 64 bit unsigned integer
        """
        # it's tempting to use time.time() to get the timestamp
        # but the docs say that its epoch is often 1970-01-01,
        # but they don't promise that it's always that
        # we use datetime.datetime() instead
        epoch = datetime.datetime(1970, 1, 1)
        now = datetime.datetime.utcnow()
        if self.initial_timestamp:
            now = now - self.start_timestamp + self.initial_timestamp
        timestamp = (now - epoch).total_seconds()
        timestamp_int = round(timestamp * 1e3)
        control = b'\x09'
        return control + struct.pack('>Q', timestamp_int)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return

        control = [numpy.uint8(0)] if self.control_byte else []
        frame = bytes([FEND] + control + kiss_escape(pmt.u8vector_elements(msg)) + [FEND])

        if self.include_timestamp:
            timestamp_frame = bytes([FEND] + kiss_escape(self.create_timestamp()) + [FEND])
            self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(timestamp_frame), timestamp_frame)))
            
        self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(frame), frame)))
