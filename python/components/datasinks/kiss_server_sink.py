#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks
from ... import pdu_to_kiss


class kiss_server_sink(gr.hier_block2):
    """
    Hierarchical block for KISS TCP server

    The input are PDUs with frames.

    These are sent to TCP clients connected to the
    TCP server

    Args:
        address: address to bind to, use '' for all (str)
        port: port to listen on (int)
        options: options from argparse
    """
    def __init__(self, address, port, options=None):
        gr.hier_block2.__init__(
            self,
            'kiss_file_sink',
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_in('in')

        self.kiss = pdu_to_kiss(include_timestamp=True)
        self.server = blocks.socket_pdu(
            'TCP_SERVER', address, port, 10000, False)

        self.msg_connect((self, 'in'), (self.kiss, 'in'))
        self.msg_connect((self.kiss, 'out'), (self.server, 'pdus'))
