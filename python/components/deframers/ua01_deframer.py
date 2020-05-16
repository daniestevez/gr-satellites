#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Daniel Estevez <daniel@destevez.net>.
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
from ... import nrzi_decode, hdlc_deframer

class ua01_deframer(gr.hier_block2):
    """
    Hierarchical block to deframe UA01 non-conformant AX.25.

    The input is a float stream of soft symbols. The output are PDUs
    with UA01 frames.

    The input should be doubly NRZ-I encoded and G3RUH scrambled.

    Args:
        options: Options from argparse
    """
    def __init__(self, options = None):
        gr.hier_block2.__init__(self, "ax25_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_out('out')

        self.slicer = digital.binary_slicer_fb()
        self.nrzi0 = nrzi_decode()
        self.nrzi1 = nrzi_decode()
        self.descrambler = digital.descrambler_bb(0x21, 0, 16)
        self.deframer = hdlc_deframer(True, 10000)

        self.connect(self, self.slicer, self.nrzi0, self.nrzi1,
                         self.descrambler, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self, 'out'))
