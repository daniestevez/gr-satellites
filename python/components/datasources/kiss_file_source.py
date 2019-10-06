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

class kiss_file_source(gr.hier_block2):
    """
    Hierarchical block for KISS file input

    The output are PDUs with frames.

    These are read from a KISS file.

    Args:
        file: output filename (string)
    """
    def __init__(self, file, append = False):
        gr.hier_block2.__init__(self, "kiss_file_source",
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_out('out')

        self.filesource = blocks.file_source(gr.sizeof_char, file)
        self.kiss = kiss_to_pdu()

        self.connect(self.filesource, self.kiss)
        self.msg_connect((self.kiss, 'out'), (self, 'out'))
