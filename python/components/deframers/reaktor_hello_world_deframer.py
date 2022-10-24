#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019, 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital

from ... import cc11xx_packet_crop, pdu_head_tail
from ...crcs import crc16_cc11xx
from ...hier.pn9_scrambler import pn9_scrambler
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block


_syncwords = {
    'reaktor hello world': '00110101001011100011010100101110',
    # The Light-1 syncword is also used by BlueWalker 3
    'light-1': '10010011000010110101000111011110',
}


class reaktor_hello_world_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the Reaktor Hello World custom framing

    This framing is based in a TI CC1125 transceiver
    with a PN9 scrambler, and a CRC-16.

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold=None,
                 syncword='reaktor hello world',
                 options=None):
        gr.hier_block2.__init__(
            self,
            'reaktor_hello_world_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        try:
            _syncword = _syncwords[syncword]
        except KeyError:
            syncwords = ', '.join([
                f"'{a}'" for a in _syncwords.keys()])
            raise ValueError(
                f'supported syncwords are:', syncwords)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(
            packlen=255, sync=_syncword, threshold=syncword_threshold)
        self.scrambler = pn9_scrambler()
        self.crop = cc11xx_packet_crop(True)
        self.crc = crc16_cc11xx()
        self.crop2 = pdu_head_tail(3, 1)

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.scrambler, 'in'))
        self.msg_connect((self.scrambler, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self.crop2, 'in'))
        self.msg_connect((self.crop2, 'out'), (self, 'out'))

    _default_sync_threshold = 4

    @classmethod
    def add_options(cls, parser):
        """
        Adds Reaktor Hello World deframer options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')
