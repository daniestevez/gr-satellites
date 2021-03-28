#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr
import pmt


# Details of the NGHam protocol taken from
# https://github.com/skagmo/ngham/blob/master/ngham.c

_tags = [
    0b001110110100100111001101,
    0b010011011101101001010111,
    0b011101101001001110011010,
    0b100110111011010010101110,
    0b101000001111110101100011,
    0b110101100110111011111001,
    0b111011010010011100110100]
ngham_tags = np.array([list(map(int, ('0'*24 + bin(t)[2:])[-24:]))
                       for t in _tags],
                      dtype='uint8')
ngham_rs_sizes = [47, 79, 111, 159, 191, 223, 255]


class ngham_packet_crop(gr.basic_block):
    """
    Crops an NGHam packet according to its size tag

    Input: An NGHam packet with size tag and RS codeword
    Output: The RS codeword appropriately cropped, routed to
    rs16 or rs32 according to the RS parity check bytes
    """
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='ngham_packet_handler',
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('rs16'))
        self.message_port_register_out(pmt.intern('rs32'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))

        size_tag = np.unpackbits(np.frombuffer(packet[:3], dtype='uint8'))
        tag_dist = np.sum(size_tag ^ ngham_tags, axis=1)
        best_tag = np.argmin(tag_dist)

        rs_size = ngham_rs_sizes[best_tag]
        if len(packet[3:]) < rs_size:
            print('Packet is too short')
            return

        out = 'rs16' if best_tag < 3 else 'rs32'
        self.message_port_pub(
            pmt.intern(out),
            pmt.cons(pmt.car(msg_pmt),
                     pmt.init_u8vector(rs_size, packet[3:3+rs_size])))
