#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2023, 2025 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital
import pmt

from ... import decode_rs, pdu_head_tail
from ...crcs import crc16_ccitt_false
from .ccsds_rs_deframer import _syncword
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block


# 0xBF35 in MSB first
_syncword = '1011111100110101'


class hades_packet_crop(gr.basic_block):
    """Crop HADES packet"""
    def __init__(self, satellite='HADES-D'):
        gr.basic_block.__init__(
            self,
            name='hades_packet_crop',
            in_sig=[],
            out_sig=[])
        self.satellite = satellite
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))
        packet_type = packet[0] >> 4
        if self.satellite == 'HADES-D':
            # https://www.amsat-ea.org/app/download/13595777/AMSAT+EA+-+HADES-D+Transmissions+description.pdf
            lengths = {1: 26, 2: 13, 3: 26, 4: 54, 5: 33, 6: 135, 7: 67, 8: 28,
                       9: 123, 12: 64}
        elif self.satellite == 'HADES-R':
            # https://www.amsat-ea.org/app/download/13945587/AMSAT+EA+-+Transmissions+description+for+MARIA-G_UNNE-1_HADES-R_HADES-ICM.pdf
            lengths = {1: 31, 2: 17, 3: 29, 4: 35, 5: 27, 6: 135, 7: 101,
                       8: 31, 9: 123, 10: 17, 11: 9, 12: 64, 14: 38, 15: 41}
        else:
            raise RuntimeError(f'invalid satellite {self.satellite}')
        try:
            packet_length = lengths[packet_type]
        except KeyError:
            # invalid packet_type
            return
        packet = packet[:packet_length]
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.car(msg_pmt),
                     pmt.init_u8vector(len(packet), list(packet))))


class hades_descrambler(gr.basic_block):
    """Descramble HADES packet"""
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='hades_packet_crop',
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
        packet = bytearray(bytes(pmt.u8vector_elements(msg)))
        # The algorithm deviates from a typical scrambler (and in fact the
        # implementation has some bugs), so it is impossible to get it right
        # just by looking at the documentation.
        #
        # See
        # https://github.com/AMSAT-EA/URESAT-1-decoder/blob/main/bit-version/linux/genesis_scrambler.c
        # for the AMSAT-EA implementation.

        # In the AMSAT-EA code the state is initialized to 0x2C350000, but
        # since the shift register is supposed to have 17 bits, most of the
        # non-zero MSBs do not matter.
        state = 1 << 16
        # The first byte is not scrambled (the CRC is not scrambled either, but
        # it has been removed at this point)
        for j in range(1, len(packet)):
            out = 0
            # There is a bug in how the scrambler is written.  The LSB is each
            # byte is not scrambler, and the scrambler state is not advanced.
            for k in range(7):
                b = (packet[j] >> (7 - k)) & 1
                b0 = b
                b ^= ((state >> 16) ^ (state >> 11)) & 1
                out = (out << 1) | b
                state = ((state << 1) | b0) & 0x1ffff
            # Take LSB directly without scrambling
            out = (out << 1) | (packet[j] & 1)
            packet[j] = out
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.car(msg_pmt),
                     pmt.init_u8vector(len(packet), list(packet))))


class hades_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe HADES custom frames

    https://www.amsat-ea.org/app/download/13595424/AMSAT+EA+-+Descripci%C3%B3n+de+transmisiones+de+HADES-D.pdf
    https://www.amsat-ea.org/app/download/13595777/AMSAT+EA+-+HADES-D+Transmissions+description.pdf
    https://www.amsat-ea.org/app/download/13945587/AMSAT+EA+-+Transmissions+description+for+MARIA-G_UNNE-1_HADES-R_HADES-ICM.pdf

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        satellite: satellite to use (either 'HADES-D' or 'HADES-R')
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, satellite='HADES-D', syncword_threshold=None,
                 options=None):
        gr.hier_block2.__init__(
            self,
            'hades_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(
            packlen=135, sync=_syncword,
            threshold=syncword_threshold)
        self.crop = hades_packet_crop(satellite)
        self.crc = crc16_ccitt_false()
        self.descrambler = hades_descrambler()

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self.descrambler, 'in'))
        self.msg_connect((self.descrambler, 'out'), (self, 'out'))

    _default_sync_threshold = 0

    @classmethod
    def add_options(cls, parser):
        """
        Adds HADES deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')
