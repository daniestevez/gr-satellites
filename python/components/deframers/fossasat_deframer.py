#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 jgromes <gromes.jan@gmail.com>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital
from ... import sx12xx_check_crc, sx12xx_packet_crop, sx12xx_remove_length
from ... import reflect_bytes
from ...hier.pn9_scrambler import pn9_scrambler
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block
import pmt

_syncword = '01010101010101010001001000010010'

class fossasat_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe FOSSASAT-1/2 custom framing

    This framing is based on Semtech SX126x transceiver
    with PN9 scrambler, bit order swapping and a CRC-16.

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "fossasat_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.sync = sync_to_pdu_packed(packlen = 255, sync = _syncword, threshold = syncword_threshold)
        self.reflect_1 = reflect_bytes()
        self.scrambler = pn9_scrambler()
        self.reflect_2 = reflect_bytes()
        self.crop = sx12xx_packet_crop(crc_len = 2)
        self.crc = sx12xx_check_crc(verbose = self.options.verbose_crc, initial = 0x1D0F, final = 0xFFFF)
        self.remove_length = sx12xx_remove_length()

        self.connect(self, self.slicer, self.sync)
        self.msg_connect((self.sync, 'out'), (self.reflect_1, 'in'))
        self.msg_connect((self.reflect_1, 'out'), (self.scrambler, 'in'))
        self.msg_connect((self.scrambler, 'out'), (self.reflect_2, 'in'))
        self.msg_connect((self.reflect_2, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self.remove_length, 'in'))
        self.msg_connect((self.remove_length, 'out'), (self, 'out'))

    _default_sync_threshold = 0

    @classmethod
    def add_options(cls, parser):
        """
        Adds FOSSASAT deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
        parser.add_argument('--verbose_crc', action = 'store_true', help = 'Verbose CRC decoder')
