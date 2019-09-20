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

import datetime

class print_timestamp(gr.basic_block):
    """
    docstring for block print_timestamp
    """
    def __init__(self, tstamp_format='', count_packets=False):
        gr.basic_block.__init__(self,
            name="swap_crc",
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
            timestamp = datetime.datetime.utcnow()
            print((timestamp.strftime(self.tstamp_format)))
        if self.count_packets:
            print('Packet number', self.packet_counter)
            self.packet_counter += 1
        
        self.message_port_pub(pmt.intern('out'), msg_pmt)
