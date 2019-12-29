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

from gnuradio import gr, blocks, digital
from ... import nrzi_decode, hdlc_deframer, header_remover, decode_rs
from ...utils.options_block import options_block

class ops_sat_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe OPS-SAT AX.25 + Reed-Solomon.

    The input is a float stream of soft symbols. The output are PDUs
    with Reed-Solomon decoded data.

    The input should be NRZ-I encoded and G3RUH scrambled.

    Args:
        options: Options from argparse
    """
    def __init__(self, options = None):
        gr.hier_block2.__init__(self, "ops_sat_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        self.slicer = digital.binary_slicer_fb()
        self.nrzi = nrzi_decode()
        self.descrambler = digital.descrambler_bb(0x21, 0, 16)
        self.deframer = hdlc_deframer(False, 10000) # we skip CRC-16 check
        self.strip = header_remover(16)

        # CCSDS descrambler
        self.pdu2tag = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.unpack = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.scramble = digital.additive_scrambler_bb(0xA9, 0xFF, 7, count=0, bits_per_byte=1, reset_tag_key="packet_len")
        self.pack = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.tag2pdu = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')

        self.fec = decode_rs(self.options.verbose_rs, 0)

        self.connect(self, self.slicer, self.nrzi, self.descrambler, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.strip, 'in'))
        self.msg_connect((self.strip, 'out'), (self.pdu2tag, 'pdus'))
        self.connect(self.pdu2tag, self.unpack, self.scramble, self.pack, self.tag2pdu)
        self.msg_connect((self.tag2pdu, 'pdus'), (self.fec, 'in'))
        self.msg_connect((self.fec, 'out'), (self, 'out'))
    @classmethod
    def add_options(cls, parser):
        """
        Adds OPS-SAT deframer specific options to the argparse parser
        """
        parser.add_argument('--verbose_rs', action = 'store_true', help = 'Verbose RS decoder')
