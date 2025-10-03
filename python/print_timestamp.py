#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import datetime

import numpy
from gnuradio import gr
import pmt


class print_timestamp(gr.basic_block):
    """docstring for block print_timestamp"""
    def __init__(self, tstamp_format='', count_packets=False):
        gr.basic_block.__init__(
            self,
            name='print_timestamp',
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))
        self.count_packets = count_packets
        self.packet_counter = 0

        self.tstamp_format = tstamp_format

    def handle_msg(self, msg_pmt):
        if self.tstamp_format:
            timestamp = datetime.datetime.now(datetime.timezone.utc)
            timestamp = timestamp.replace(tzinfo=None)
            print((timestamp.strftime(self.tstamp_format)))
        if self.count_packets:
            print('Packet number', self.packet_counter)
            self.packet_counter += 1

        self.message_port_pub(pmt.intern('out'), msg_pmt)
