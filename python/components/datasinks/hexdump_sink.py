#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks

class hexdump_sink(gr.hier_block2):
    """
    Hierarchical block for hexdump output

    The input are PDUs with frames.

    These are printed in hex.

    Args:
    """
    def __init__(self):
        gr.hier_block2.__init__(self, "hexdump_sink",
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_in('in')

        self.message_debug = blocks.message_debug()
        self.msg_connect((self, 'in'), (self.message_debug, 'print_pdu'))
