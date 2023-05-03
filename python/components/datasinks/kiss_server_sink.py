#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020, 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks
from ... import pdu_to_kiss
from ...utils.options_block import options_block


class kiss_server_sink(gr.hier_block2, options_block):
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
        options_block.__init__(self, options)

        initial_timestamp = getattr(self.options, 'start_time', '')

        self.kiss = pdu_to_kiss(include_timestamp=True,
                                initial_timestamp=initial_timestamp)
        # port needs to be an str
        port = str(port)
        self.server = blocks.socket_pdu(
            'TCP_SERVER', address, port, 10000, False)

        self.msg_connect((self, 'in'), (self.kiss, 'in'))
        self.msg_connect((self.kiss, 'out'), (self.server, 'pdus'))

    @classmethod
    def add_options(cls, parser):
        """
        Adds KISS server sink specific options to the argparse parser
        """
        parser.add_argument(
            '--start_time', type=str, default='',
            help='Recording start timestamp')
