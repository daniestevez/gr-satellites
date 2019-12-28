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
from ... import decode_rs, ngham_packet_crop, ngham_remove_padding, ngham_check_crc
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...hier.ccsds_descrambler import ccsds_descrambler
from ...utils.options_block import options_block

_syncword = '01011101111001100010101001111110'

class ngham_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe NGHam frames

    These use a CCSDS scrambler and CCSDS Reed-Solomon
    Reed-Solomon decoding is currently not implemented

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        decode_rs: use Reed-Solomon decoding (bool)
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, decode_rs = False, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "ccsds_rs_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        if decode_rs:
            raise ValueError('NGHam Reed-Solomon decoding not implemented yet')
        
        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(packlen = 255 + 3,\
                                           sync = _syncword,\
                                           threshold = syncword_threshold)
        self.crop = ngham_packet_crop()
        self.pdu2tag = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.unpack = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.taglength = blocks.tagged_stream_multiply_length(gr.sizeof_char*1, 'packet_len', 8)
        self.tag2pdu = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')
        self.scrambler = ccsds_descrambler()
        self.padding = ngham_remove_padding()
        self.crc = ngham_check_crc(self.options.verbose_crc)

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'rs16'), (self.pdu2tag, 'pdus'))
        self.msg_connect((self.crop, 'rs32'), (self.pdu2tag, 'pdus'))
        self.connect(self.pdu2tag, self.unpack, self.taglength, self.tag2pdu)
        self.msg_connect((self.tag2pdu, 'pdus'), (self.scrambler, 'in'))
        self.msg_connect((self.scrambler, 'out'), (self.padding, 'in'))
        self.msg_connect((self.padding, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self, 'out'))

    _default_sync_threshold = 4
        
    @classmethod
    def add_options(cls, parser):
        """
        Adds NGHam deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
#        parser.add_argument('--verbose_rs', action = 'store_true', help = 'Verbose RS decoder')
        parser.add_argument('--verbose_crc', action = 'store_true', help = 'Verbose CRC check')
