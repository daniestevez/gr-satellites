#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr
import pmt

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
            print("[ERROR] Received invalid message type. Expected u8vector")
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
        
        packet = bytes(packet)
        self.message_port_pub(pmt.intern('out'),  pmt.cons(pmt.car(msg_pmt), pmt.init_u8vector(len(packet), packet)))

