#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Daniel Estevez <daniel@destevez.net>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

from gnuradio import gr, blocks
from ... import kiss_to_pdu

class kiss_transport(gr.hier_block2):
    """
    Hierarchical block for KISS transport.

    The input are PDUs with a KISS stream. The output are PDUs
    with the frames encapsulated in the stream.

    Args:
        control_byte: Expect KISS control byte (bool)
    """
    def __init__(self, control_byte = True):
        gr.hier_block2.__init__(self, "kiss_transport",
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_in('in')
        self.message_port_register_hier_out('out')

        self.pdu2tag = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.kiss = kiss_to_pdu(control_byte)

        self.msg_connect((self, 'in'), (self.pdu2tag, 'pdus'))
        self.connect(self.pdu2tag, self.kiss)
        self.msg_connect((self.kiss, 'out'), (self, 'out'))
