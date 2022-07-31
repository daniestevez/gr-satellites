#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital
import numpy as np
import pmt

from ... import viterbi_decoder
from ...crcs import crc16_ccitt_x25
from ...hier.sync_to_pdu import sync_to_pdu
from ...utils.options_block import options_block


# Syncword is 0xe37b167e followed by a 1
# (UART stop bit for 0x7e)
# This is UART encoded
_syncword = '111000110111101100010110011111101'


_scrambler_seq = np.array(
    [0x0e, 0xf2, 0xc9, 0x02, 0x26, 0x2e, 0xb6, 0x0c, 0xd4, 0xe7,
     0xb4, 0x2a, 0xfa, 0x51, 0xb8, 0xfe, 0x1d, 0xe5, 0x92, 0x04,
     0x4c, 0x5d, 0x6c, 0x19, 0xa9, 0xcf, 0x68, 0x55, 0xf4, 0xa3,
     0x71, 0xfc, 0x3b, 0xcb, 0x24, 0x08, 0x98, 0xba, 0xd8, 0x33,
     0x53, 0x9e, 0xd0, 0xab, 0xe9, 0x46, 0xe3, 0xf8, 0x77, 0x96,
     0x48, 0x11, 0x31, 0x75, 0xb0, 0x66, 0xa7, 0x3d, 0xa1, 0x57,
     0xd2, 0x8d, 0xc7, 0xf0, 0xef, 0x2c, 0x90, 0x22, 0x62, 0xeb,
     0x60, 0xcd, 0x4e, 0x7b, 0x42, 0xaf, 0xa5, 0x1b, 0x8f, 0xe1,
     0xde, 0x59, 0x20, 0x44, 0xc5, 0xd6, 0xc1, 0x9a, 0x9c, 0xf6,
     0x85, 0x5f, 0x4a, 0x37, 0x1f, 0xc3, 0xbc, 0xb2, 0x40, 0x89,
     0x8b, 0xad, 0x83, 0x35, 0x39, 0xed, 0x0a, 0xbe, 0x94, 0x6e,
     0x3f, 0x87, 0x79, 0x64, 0x81, 0x13, 0x17, 0x5b, 0x06, 0x6a,
     0x73, 0xda, 0x15, 0x7d, 0x28, 0xdc, 0x7f],
    dtype='uint8')


class prepare_fec(gr.basic_block):
    """
    Helper block to prepare the convolutional encoded FEC codeword.

    This performs UART 8N1 decoding, deinterleaving and descrambling.
    """
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='prepare_fec',
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = np.array(pmt.u8vector_elements(msg), dtype='uint8')
        assert packet.size % 10 == 0

        uart_decode = np.packbits(
            packet.reshape(-1, 10)[:, 1:-1][:, ::-1])
        fec_data = uart_decode[16:16+102]
        # Deinterleave: the last 6 bytes are not interleaved, since the
        # interleaver works in blocks of 8 bytes
        data_a, data_b = fec_data[:-6], fec_data[-6:]
        data_a = np.packbits(
            np.einsum('ijk->ikj',
                      np.unpackbits(data_a).reshape(-1, 8, 8)[:, :, ::-1])
            [:, :, ::-1])
        deinter = np.concatenate((data_a, data_b))
        descrambled = deinter ^ _scrambler_seq[:102]

        # The input to the convolutional code always ends with a 0x00 byte to
        # terminate the trellis. This produces 16 encoded bits. However, only
        # 2 bits are needed to terminate the trellis (K = 3), which produce 4
        # encoded bits. Thus, we can throw away the last 12 bits.
        viterbi_in = bytes(np.unpackbits(descrambled)[:-12])

        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.car(msg_pmt),
                     pmt.init_u8vector(len(viterbi_in), viterbi_in)))


class pack_viterbi_out(gr.basic_block):
    """
    Helper block to pack the Viterbi decoder output.
    """
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='pack_viterbi_out',
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = np.array(pmt.u8vector_elements(msg), dtype='uint8')
        packet = bytes(np.packbits(packet))
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.car(msg_pmt),
                     pmt.init_u8vector(len(packet), packet)))


class hsu_sat1_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe HSU-SAT1 frames.

    HSU-SAT1 uses custom frames with an 8N1 UART encoding and FEC
    following the library https://github.com/f4goh/CONVOLUTION
    This consists of an r=1/2 k=3 convolutional code, block interleaver
    and scrambler.

    The input is a float stream of soft symbols. The output are PDUs
    with HSU-SAT1 frames. Only the FEC data (with the CRC and Viterbi
    tail stripped) is included in the output.

    Args:
        options: Options from argparse
    """
    def __init__(self, options=None):
        gr.hier_block2.__init__(
            self,
            'hsu_sat1_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu(
            packlen=(16+102)*10, sync=_syncword,
            threshold=self.options.syncword_threshold)
        self.prepare = prepare_fec()
        self.viterbi = viterbi_decoder(3, [7, 5])
        self.pack = pack_viterbi_out()
        self.crc = crc16_ccitt_x25(swap_endianness=False)

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.prepare, 'in'))
        self.msg_connect((self.prepare, 'out'), (self.viterbi, 'in'))
        self.msg_connect((self.viterbi, 'out'), (self.pack, 'in'))
        self.msg_connect((self.pack, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self, 'out'))

    _default_sync_threshold = 4

    @classmethod
    def add_options(cls, parser):
        """
        Adds DIY-1 deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')
