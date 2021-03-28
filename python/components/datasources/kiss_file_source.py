#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks

from ... import kiss_to_pdu


class kiss_file_source(gr.hier_block2):
    """
    Hierarchical block for KISS file input

    The output are PDUs with frames.

    These are read from a KISS file.

    Args:
        file: input filename (string)
        options: options from argparse
    """
    def __init__(self, file, append=False, options=None):
        gr.hier_block2.__init__(
            self,
            'kiss_file_source',
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_out('out')

        self.filesource = blocks.file_source(gr.sizeof_char, file)
        self.kiss = kiss_to_pdu()

        self.connect(self.filesource, self.kiss)
        self.msg_connect((self.kiss, 'out'), (self, 'out'))
