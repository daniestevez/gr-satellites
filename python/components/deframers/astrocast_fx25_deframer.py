#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019, 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital

from ... import nrzi_decode, reflect_bytes, decode_rs, check_astrocast_crc
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block


_syncword = '0111010111111010110000011010001101011000110100000110010001110110'


class astrocast_fx25_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the Astrocast (somewhat non-compliant) FX.25

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        nrzi: use NRZ-I instead of NRZ (bool)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold=None, nrzi=True, options=None):
        gr.hier_block2.__init__(
            self,
            'astrocast_fx25_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        if nrzi:
            self.nrzi = nrzi_decode()
        self.deframer = sync_to_pdu_packed(
            packlen=255, sync=_syncword, threshold=syncword_threshold)
        self.reflect = reflect_bytes()
        self.rs = decode_rs(True, 1)
        self.crc = check_astrocast_crc(self.options.verbose_crc)

        blocks = [self, self.slicer]
        if nrzi:
            blocks.append(self.nrzi)
        blocks.append(self.deframer)

        self.connect(*blocks)
        self.msg_connect((self.deframer, 'out'), (self.reflect, 'in'))
        self.msg_connect((self.reflect, 'out'), (self.rs, 'in'))
        self.msg_connect((self.rs, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self, 'out'))

    _default_sync_threshold = 8

    @classmethod
    def add_options(cls, parser):
        """
        Adds Astrocast FX.25 deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')
        parser.add_argument(
            '--verbose_crc', action='store_true', help='Verbose CRC decoder')
