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

from gnuradio import gr, digital, fec, blocks
from ... import distributed_syncframe_soft, matrix_deinterleaver_soft, ao40_rs_decoder
from ...hier.ccsds_descrambler import ccsds_descrambler
from ...utils.options_block import options_block

_syncword = '11111110000111011110010110010010000001000100110001011101011011000'

class ao40_fec_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the AO-40 FEC protocol.

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "ao40_fec_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.deframer = distributed_syncframe_soft(syncword_threshold, _syncword, 80)
        self.deinterleaver = matrix_deinterleaver_soft(80, 65, 5132, 65)
        self.viterbi = fec.cc_decoder.make(5132,7, 2, [79,-109], 0, -1, fec.CC_TERMINATED, False)
        self.viterbi_decoder = fec.async_decoder(self.viterbi, False, False, int(5132/8))
        self.scrambler = ccsds_descrambler()
        self.rs = ao40_rs_decoder(self.options.verbose_rs)

        self.connect(self, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.deinterleaver, 'in'))
        self.msg_connect((self.deinterleaver, 'out'), (self.viterbi_decoder, 'in'))
        self.msg_connect((self.viterbi_decoder, 'out'), (self.scrambler, 'in'))
        self.msg_connect((self.scrambler, 'out'), (self.rs, 'in'))
        self.msg_connect((self.rs, 'out'), (self, 'out'))

    _default_sync_threshold = 8
        
    @classmethod
    def add_options(cls, parser):
        """
        Adds AO-40 FEC deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
        parser.add_argument('--verbose_rs', action = 'store_true', help = 'Verbose RS decoder')
