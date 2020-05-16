#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital
from ... import reflect_bytes, swiatowid_packet_crop, swiatowid_packet_split, decode_rs_general
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block

_syncword = '01011011010110111101110111011101'

class swiatowid_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the Swiatowid custom image protocol

    The input is a float stream of soft symbols. The output are PDUs
    with image frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "swiatowid_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(packlen = 8200,\
                                    sync = _syncword,\
                                    threshold = syncword_threshold)
        self.reflect = reflect_bytes()
        self.crop = swiatowid_packet_crop()
        self.split = swiatowid_packet_split()
        self.rs = decode_rs_general(0x11d, 0, 1, 10, self.options.verbose_rs)
        
        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.reflect, 'in'))
        self.msg_connect((self.reflect, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.split, 'in'))
        self.msg_connect((self.split, 'out'), (self.rs, 'in'))
        self.msg_connect((self.rs, 'out'), (self, 'out'))

    _default_sync_threshold = 0
        
    @classmethod
    def add_options(cls, parser):
        """
        Adds Swiatowid deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
        parser.add_argument('--verbose_rs', action = 'store_true', help = 'Verbose RS decoder')
