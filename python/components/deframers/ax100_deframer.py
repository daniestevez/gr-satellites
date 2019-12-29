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
from ... import ax100_decode, u482c_decode
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block

_syncword = '10010011000010110101000111011110'

class ax100_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the GOMspace AX100 protocols.

    The input is a float stream of soft symbols. The output are PDUs
    with frames (most likely CSP frames).

    Args:
        mode: mode to use ('RS' or 'ASM') (string)
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, mode, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "ax100_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        if mode not in ['RS', 'ASM']:
            raise Exception("Unsupported AX100 mode. Use 'RS' or 'ASM'")

        self.slicer = digital.binary_slicer_fb()
        if mode == 'RS':
            self.descrambler = digital.descrambler_bb(0x21, 0, 16)
        self.deframer = sync_to_pdu_packed(packlen = 256 if mode == 'RS' else 255,\
                                           sync = _syncword,\
                                           threshold = syncword_threshold)
        self.fec = ax100_decode(self.options.verbose_fec) if mode == 'RS'\
          else u482c_decode(self.options.verbose_fec, 0, 1, 1)

        self._blocks = [self, self.slicer]
        if mode == 'RS':
            self._blocks.append(self.descrambler)
        self._blocks += [self.deframer]

        self.connect(*self._blocks)
        self.msg_connect((self.deframer, 'out'), (self.fec, 'in'))
        self.msg_connect((self.fec, 'out'), (self, 'out'))

    _default_sync_threshold = 4
        
    @classmethod
    def add_options(cls, parser):
        """
        Adds AX100 deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
        parser.add_argument('--verbose_fec', action = 'store_true', help = 'Verbose FEC decoder')
