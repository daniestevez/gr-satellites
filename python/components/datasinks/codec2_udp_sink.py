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
from ...utils.options_block import options_block

class codec2_udp_sink(gr.hier_block2, options_block):
    """
    Hierarchical block for Codec2 UDP output

    The input are PDUs with Codec2 data

    The Codec2 data is sent to by PDU, a single frame (7 bytes)
    per packet for lowest latency.

    Args:
      ip: Detination IP (string)
      port: Destination UDP port (int)
    """
    def __init__(self, ip = None, port = None, options = None):
        gr.hier_block2.__init__(self, "codec2_udp_sink",
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        self.message_port_register_hier_in('in')

        if ip is None:
            ip = self.options.codec2_ip
        if port is None:
            port = self.options.codec2_port
            
        self.pdu2tag = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        payload_bytes = 7
        self.udp = blocks.udp_sink(gr.sizeof_char*1, ip, port, payload_bytes, False)
        self.msg_connect((self, 'in'), (self.pdu2tag, 'pdus'))
        self.connect(self.pdu2tag, self.udp)

    _default_ip = '127.0.0.1'
    _default_port = 7000
    
    @classmethod
    def add_options(cls, parser):
        """
        Adds Codec2 UDP output specific options to the argparse parser
        """
        parser.add_argument('--codec2_ip', type = str, default = cls._default_ip, help = 'Codec2 output IP [default=%(default)r]')
        parser.add_argument('--codec2_port', type = int, default = cls._default_port, help = 'Codec2 output UDP port [default=%(default)r]')
