#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr
import pmt

# This block is based on the Universal SPUNTIX Protocol (USP)
# Protocol Description revision 1.04
# https://sputnix.ru/tpl/docs/amateurs/USP%20protocol%20description%20v1.04.pdf

# Generator matrix for the (64,7) PLS linear code
G = '0011001100110011001100110011001100110011001100110011001100110011000011110000111100001111000011110000111100001111000011110000111100000000111111110000000011111111000000001111111100000000111111110000000000000000111111111111111100000000000000001111111111111111000000000000000000000000000000001111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110101010101010101010101010101010101010101010101010101010101010101'
G = np.array([int(a) for a in G], dtype = 'uint8').reshape((-1,64)).T

# Defined PLS codes
PLS_codes = np.array([0,1], dtype = 'uint8')
PLS_vectors = np.unpackbits(np.array(PLS_codes, dtype = 'uint8')[np.newaxis,:], axis = 0)[1:]

# Encoded and scrambled PLS 64-bit vectors
enc_PLS = (G @ PLS_vectors) % 2
scramble_seq = '0111000110011101100000111100100101010011010000100010110111111010'
scramble_seq = np.array([int(a) for a in scramble_seq], dtype = 'uint8')
scrambled_PLS = enc_PLS ^ scramble_seq[:,np.newaxis]
scrambled_PLS_bipolar = 2 * scrambled_PLS.astype('float32') - 1

class usp_pls_crop(gr.basic_block):
    """
    Crop a USP packet according to its PLS
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="usp_pls_crop",
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_f32vector(msg):
            print("[ERROR] Received invalid message type. Expected f32vector")
            return
        pls = np.array(pmt.f32vector_elements(msg)[:64], dtype = 'float32')
        correlations = np.sum(pls[:,np.newaxis] * scrambled_PLS_bipolar, axis = 0)
        code = PLS_codes[np.argmax(correlations)]

        # It seems that there is a typo in the rev 1.04 document
        # PLS-code 0 is listed as corresponding to data length 223
        # PLS-code 1 is listed as corresponding to data length 48
        # However, according to the test IQ data it is the other way
        # around
        data_len = 48 if code == 0 else 223
        payload_len = (data_len + 32) * 2
        payload_out = pmt.f32vector_elements(msg)[64:][:8*payload_len]
        payload_out = pmt.init_f32vector(len(payload_out), payload_out)
        msg_out = pmt.cons(pmt.car(msg_pmt), payload_out)
        self.message_port_pub(pmt.intern('out'), msg_out)
