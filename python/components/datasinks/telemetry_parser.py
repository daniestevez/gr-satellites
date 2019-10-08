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

from gnuradio import gr
import pmt
from ... import telemetry
import sys
from construct.core import ConstructError

class telemetry_parser(gr.basic_block):
    """
    Block for telemetry parsing

    The input are PDUs with frames

    These are parsed with construct and the text output is printed
    or saved to file

    Args:
        definition: telemetry definition name (to load from the telemetry package) (str)
        file: file to print output (defaults to sys.stdout)
    """
    def __init__(self, definition, file = sys.stdout):
        gr.basic_block.__init__(self, "telemetry_submit",
            in_sig = [],
            out_sig = [])
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.format = getattr(telemetry, definition)
        self.file = file

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytes(pmt.u8vector_elements(msg))

        try:
            data = self.format.parse(packet)
        except ConstructError as e:
            print(f'Could not parse telemetry beacon {e}', file = self.file)
            return
        if data:
            print(data, file = self.file)
