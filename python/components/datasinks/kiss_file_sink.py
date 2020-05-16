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

class kiss_file_sink(gr.hier_block2):
    """
    Hierarchical block for KISS file output

    The input are PDUs with frames.

    These are saved to a KISS file.

    Args:
        file: output filename (string)
        append: append to file (bool)
    """
    def __init__(self, file, append = False):
        gr.hier_block2.__init__(self, "kiss_file_sink",
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_in('in')

        self.kiss = pdu_to_kiss()
        self.pdu2tag = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.filesink = blocks.file_sink(gr.sizeof_char, file, append)

        self.connect(self.pdu2tag, self.filesink)
        self.msg_connect((self, 'in'), (self.kiss, 'in'))
        self.msg_connect((self.kiss, 'out'), (self.pdu2tag, 'pdus'))
