#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks

from ... import pdu_to_kiss
from ...utils.options_block import options_block


class kiss_file_sink(gr.hier_block2, options_block):
    """
    Hierarchical block for KISS file output

    The input are PDUs with frames.

    These are saved to a KISS file.

    Args:
        file: output filename (string)
        append: append to file (bool)
        options: options from argparse
    """
    def __init__(self, file, append=False, options=None):
        gr.hier_block2.__init__(
            self,
            'kiss_file_sink',
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_in('in')

        initial_timestamp = getattr(self.options, 'start_time', '')

        self.kiss = pdu_to_kiss(include_timestamp=True,
                                initial_timestamp=initial_timestamp)
        self.pdu2tag = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.filesink = blocks.file_sink(gr.sizeof_char, file, append)

        self.connect(self.pdu2tag, self.filesink)
        self.msg_connect((self, 'in'), (self.kiss, 'in'))
        self.msg_connect((self.kiss, 'out'), (self.pdu2tag, 'pdus'))

    @classmethod
    def add_options(cls, parser):
        """
        Adds KISS file sink specific options to the argparse parser
        """
        parser.add_argument(
            '--start_time', type=str, default='',
            help='Recording start timestamp')
