#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks
from ... import kiss_to_pdu, header_remover

class kiss_transport(gr.hier_block2):
    """
    Hierarchical block for KISS transport.

    The input are PDUs with a KISS stream. The output are PDUs
    with the frames encapsulated in the stream.

    Args:
        control_byte: Expect KISS control byte (bool)
        header_remove_bytes: Remove this many bytes from header (int)
    """
    def __init__(self, control_byte = True, header_remove_bytes = 0):
        gr.hier_block2.__init__(self, "kiss_transport",
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_in('in')
        self.message_port_register_hier_out('out')

        if header_remove_bytes:
            self.header = header_remover(header_remove_bytes)
        self.pdu2tag = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.kiss = kiss_to_pdu(control_byte)

        if header_remove_bytes:
            self.msg_connect((self, 'in'), (self.header, 'in'))
            self.msg_connect((self.header, 'out'), (self.pdu2tag, 'pdus'))
        else:
            self.msg_connect((self, 'in'), (self.pdu2tag, 'pdus'))
        self.connect(self.pdu2tag, self.kiss)
        self.msg_connect((self.kiss, 'out'), (self, 'out'))
