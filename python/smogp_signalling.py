#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 Daniel Estevez <daniel@destevez.net>
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
# 

import numpy
from gnuradio import gr
import pmt
import numpy as np

signalling_prbs = np.array([0x97, 0xfd, 0xd3, 0x7b, 0x0f, 0x1f, 0x6d,\
                            0x08, 0xf7, 0x83, 0x5d, 0x9e, 0x59, 0x82,\
                            0xc0, 0xfd, 0x1d, 0xca, 0xad, 0x3b, 0x5b,\
                            0xeb, 0xd4, 0x93, 0xe1, 0x4a, 0x04, 0xd2,\
                            0x28, 0xdd, 0xf9, 0x01, 0x53, 0xd2, 0xe6,\
                            0x6c, 0x5b, 0x25, 0x65, 0x31, 0xc5, 0x7c,\
                            0xe7, 0xf1, 0x38, 0x61, 0x2d, 0x5c, 0x03,\
                            0x3a, 0xc6, 0x88, 0x90, 0xdb, 0x8c, 0x8c,\
                            0x42, 0xf3, 0x51, 0x75, 0x43, 0xa0, 0x83, 0x93], dtype = 'uint8')

downlink_speeds = [500, 1250, 2500, 5000, 12500]
codings = ['RX', 'AO-40 short', 'AO-40', 'RA (260, 128)', 'RA (514, 256)']

class smogp_signalling(gr.basic_block):
    """
    Handles signalling packets from SMOG-P or ATL-1
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="smogp_signalling",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytes(pmt.u8vector_elements(msg))

        if len(packet) != 64:
            print('Error: signalling packet length != 64')
            return

        prbs = np.frombuffer(packet[:-6], dtype = 'uint8')
        ber_prbs = np.sum((np.unpackbits(prbs) ^ np.unpackbits(signalling_prbs[6:])).astype('int')) / (prbs.size * 8)

        flags = np.unpackbits(np.frombuffer(packet[-6:], dtype = 'uint8')).reshape((-1, 8))
        decoded_flags = 1*(np.sum(flags, axis = 1) > 4)

        try:
            downlink_speed = downlink_speeds[np.packbits(decoded_flags[:3])[0] >> 5]
        except IndexError:
            print(f'Error: invalid downlink speed {decoded_flags[:3]}')
            return

        try:
            coding = codings[np.packbits(decoded_flags[3:])[0] >> 5]
        except IndexError:
            print(f'Error: invalid coding {decoded_flags[3:]}')
            return

        print(f'Signalling packet: BER {ber_prbs:.4f}, rate {downlink_speed} baud, coding {coding}')
