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

from gnuradio import gr, digital
from ... import check_cc11xx_crc, cc11xx_packet_crop, cc11xx_remove_length
from ...hier.pn9_scrambler import pn9_scrambler
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block

_syncword = '00110101001011100011010100101110'

class reaktor_hello_world_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the Reaktor Hello World custom framing

    This framing is based in a TI CC1125 transceiver
    with a PN9 scrambler, and a CRC-16.

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "reaktor_hello_world_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(packlen = 255,\
                                           sync = _syncword,\
                                           threshold = syncword_threshold)
        self.scrambler = pn9_scrambler()
        self.crop = cc11xx_packet_crop(True)
        self.crc = check_cc11xx_crc(self.options.verbose_crc)
        self.crop2 = cc11xx_remove_length()

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.scrambler, 'in'))
        self.msg_connect((self.scrambler, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self.crop2, 'in'))
        self.msg_connect((self.crop2, 'out'), (self, 'out'))

    _default_sync_threshold = 4
    
    @classmethod
    def add_options(cls, parser):
        """
        Adds Reaktor Hello World deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
        parser.add_argument('--verbose_crc', action = 'store_true', help = 'Verbose CRC decoder')
