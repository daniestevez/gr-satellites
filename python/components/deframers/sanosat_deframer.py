#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2022 Daniel Estevez <daniel@destevez.net>
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

# 0xB22B in MSB first
_syncword = '1011010000101011'


class sanosat_packet_crop(gr.basic_block):
    """Crop SanoSat-1 packet"""
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='sanosat_packet_crop',
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
        packet = bytes(pmt.u8vector_elements(msg))
        # 5 bytes consists of 1 byte for lenght field
        # plus 4 bytes for delimiter FFFF0000
        packet_length = packet[0] + 5
        packet = bytearray(packet[:packet_length])
        # Delete CRC1 field, which is not used in the CRC2 calculation
        del packet[1:3]
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.car(msg_pmt),
                     pmt.init_u8vector(len(packet), list(packet))))


class sanosat_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe SanoSat-1 custom frames

    See https://amsat-np.org/transmission-protocol-for-sanosat-1/

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold=None, options=None):
        gr.hier_block2.__init__(
            self,
            'sanosat_deframer',
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
        self.crop = sanosat_packet_crop()
        self.crc = crc16_ccitt_false(swap_endianness=True)
        # Remove length field and FFFF0000 delimiter
        self.crop2 = pdu_head_tail(3, 5)

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self.crop2, 'in'))
        self.msg_connect((self.crop2, 'out'), (self, 'out'))

    _default_sync_threshold = 0

    @classmethod
    def add_options(cls, parser):
        """
        Adds SanoSat-1 deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')
