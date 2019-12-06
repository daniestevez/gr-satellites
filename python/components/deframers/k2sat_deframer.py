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

from gnuradio import gr, digital, blocks, fec
from ... import descrambler308
from ... import k2sat_deframer as deframer
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block

_syncword = '0101010101111110'

class k2sat_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the K2SAT custom image protocol

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "k2sat_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        # For QPKS 90º abiguity
        self.deinterleave = blocks.deinterleave(gr.sizeof_float, 1)
        self.invert = blocks.multiply_const_ff(-1, 1)
        self.interleave = blocks.interleave(gr.sizeof_float, 1)
        
        self.cc0 = fec.cc_decoder.make(80, 7, 2, [79, 109], 0, -1, fec.CC_STREAMING, False)
        self.cc1 = fec.cc_decoder.make(80, 7, 2, [79, 109], 0, -1, fec.CC_STREAMING, False)
        self.viterbi0 = fec.extended_decoder(decoder_obj_list = self.cc0,\
                                             threading = None,\
                                             ann = None,
                                             puncpat = '11')
        self.viterbi1 = fec.extended_decoder(decoder_obj_list = self.cc1,\
                                             threading = None,\
                                             ann = None,
                                             puncpat = '11')
        self.diff0 = digital.diff_decoder_bb(2)
        self.diff1 = digital.diff_decoder_bb(2)
        self.scrambler0 = descrambler308()
        self.scrambler1 = descrambler308()
        self.deframer0 = sync_to_pdu_packed(packlen = 2200,\
                                        sync = _syncword,\
                                        threshold = syncword_threshold)
        self.deframer1 = sync_to_pdu_packed(packlen = 2200,\
                                        sync = _syncword,\
                                        threshold = syncword_threshold)
        self.deframer = deframer()
        
        self.connect(self, self.viterbi0, self.diff0, self.scrambler0, self.deframer0)
        self.connect(self, self.deinterleave)
        self.connect((self.deinterleave, 0), (self.interleave, 1))
        self.connect((self.deinterleave, 1), self.invert, (self.interleave, 0))
        self.connect(self.interleave, self.viterbi1, self.diff1, self.scrambler1, self.deframer1)
        
        self.msg_connect((self.deframer0, 'out'), (self.deframer, 'in'))
        self.msg_connect((self.deframer1, 'out'), (self.deframer, 'in'))
        self.msg_connect((self.deframer, 'out'), (self, 'out'))

    _default_sync_threshold = 0
        
    @classmethod
    def add_options(cls, parser):
        """
        Adds K2SAT deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
