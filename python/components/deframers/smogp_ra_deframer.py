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
from ... import decode_ra_code, smogp_packet_filter
from ...hier.sync_to_pdu_soft import sync_to_pdu_soft
from ...utils.options_block import options_block

_syncword = '0010110111010100'
fec_sizes = {128: 260, 256: 514}

class smogp_ra_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the SMOG-P RA FEC frames

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        frame_size: size of the frame before FEC (int)
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, frame_size, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "smogp_ra_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.deframer = sync_to_pdu_soft(packlen = fec_sizes[frame_size] * 8,\
                                         sync = _syncword,\
                                         threshold = syncword_threshold)
        self.fec = decode_ra_code(frame_size)
        self.filter = smogp_packet_filter()

        self.connect(self, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.fec, 'in'))
        self.msg_connect((self.fec, 'out'), (self.filter, 'in'))
        self.msg_connect((self.filter, 'out'), (self, 'out'))

    _default_sync_threshold = 0
        
    @classmethod
    def add_options(cls, parser):
        """
        Adds SMOG-P RA deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
