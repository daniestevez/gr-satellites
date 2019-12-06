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
from .ccsds_rs_deframer import ccsds_rs_deframer
from ...hier.ccsds_viterbi import ccsds_viterbi
from ...utils.options_block import options_block

class ccsds_concatenated_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe CCSDS concatenated
    (convolutional + Reed-Solomon) TM frames

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        frame_size: frame size (not including parity check bytes) (int)
        differential: whether to use differential coding (bool)
        dual_basis: use dual basis instead of conventional (bool)
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, frame_size = 223, differential = False, dual_basis = False, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "ccsds_concatenated_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        self.delay1 =  blocks.delay(gr.sizeof_float, 1)
        self.viterbi0 = ccsds_viterbi()
        self.viterbi1 = ccsds_viterbi()
        self.char2float0 = blocks.char_to_float(1, 1)
        self.char2float1 = blocks.char_to_float(1, 1)
        self.addconst0 = blocks.add_const_ff(-0.5)
        self.addconst1 = blocks.add_const_ff(-0.5)
        self.rs0 = ccsds_rs_deframer(frame_size, differential, dual_basis, syncword_threshold, options)
        self.rs1 = ccsds_rs_deframer(frame_size, differential, dual_basis, syncword_threshold, options)

        self.connect(self, self.viterbi0, self.char2float0, self.addconst0, self.rs0)
        self.connect(self, self.delay1, self.viterbi1, self.char2float1, self.addconst1, self.rs1)
        self.msg_connect((self.rs0, 'out'), (self, 'out'))
        self.msg_connect((self.rs1, 'out'), (self, 'out'))

    @classmethod
    def add_options(cls, parser):
        """
        Adds CCSDS concatenated deframer specific options to the argparse parser
        """
        ccsds_rs_deframer.add_options(parser)
