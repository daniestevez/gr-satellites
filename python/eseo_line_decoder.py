#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Daniel Estevez <daniel@destevez.net>.
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

import numpy as np
from gnuradio import gr
import pmt
import array

def reflect_bytes(x):
    return np.fliplr(x[:x.size//8*8].reshape((-1,8))).ravel()

def destuff(x):
    y = list()
    run = 0
    for i, bit in enumerate(x):
        if run == 5:
            if bit == 1:
                # unexpected long run of ones
                return
            else:
                run = 0
        elif bit == 0:
            run = 0
            y.append(bit)
        elif bit == 1:
            run += 1
            y.append(bit)
    return np.array(y, dtype = 'uint8')

def descramble(x):
    y = np.concatenate((np.zeros(17, dtype='uint8'), x))
    z = y[:-17] ^ y[5:-12] ^ y[17:]
    return z

def nrzi_decode(x):
    return x ^ np.concatenate((np.zeros(1, dtype = 'uint8'), x[:-1])) ^ 1

class eseo_line_decoder(gr.basic_block):
    """
    docstring for block eseo_line_decoder
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="eseo_line_decoder",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = np.array(pmt.u8vector_elements(msg), dtype = 'uint8')

        # Decode ESEO "line coding"
        packet = np.unpackbits(packet)
        packet = destuff(packet)
        if packet is None:
            return
        packet = descramble(packet)
        packet = nrzi_decode(packet)
        packet = reflect_bytes(packet)
        # Remove dummy padding
        cutbits = packet.size % 8
        if cutbits:
            packet = packet[:-cutbits]
        packet = np.packbits(packet)
        
        packet = array.array('B', packet)
        self.message_port_pub(pmt.intern('out'),  pmt.cons(pmt.car(msg_pmt), pmt.init_u8vector(len(packet), packet)))

