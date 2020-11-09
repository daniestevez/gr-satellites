#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import pmt
from ... import telemetry
import sys
from construct.core import ConstructError
import os

class telemetry_parser(gr.basic_block):
    """
    Block for telemetry parsing

    The input are PDUs with frames

    These are parsed with construct and the text output is printed
    or saved to file

    Args:
        definition: telemetry definition name (to load from the telemetry package) (str)
        file: file or file path to print output (defaults to sys.stdout)
        options: options from argparse
    """
    def __init__(self, definition, file = sys.stdout, options = None):
        gr.basic_block.__init__(self, "telemetry_parser",
            in_sig = [],
            out_sig = [])
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.format = getattr(telemetry, definition)
        if getattr(options, 'telemetry_output', None):
            file = options.telemetry_output
        if type(file) in [str, bytes] or isinstance(file, os.PathLike):
            file = open(file, 'a')
        self.file = file

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytes(pmt.u8vector_elements(msg))

        meta = pmt.car(msg_pmt)
        transmitter = pmt.dict_ref(meta, pmt.intern('transmitter'), pmt.PMT_NIL)
        if pmt.is_symbol(transmitter):
            print('-> Packet from', pmt.symbol_to_string(transmitter),
                      file = self.file) 
        
        try:
            data = self.format.parse(packet)
        except ConstructError as e:
            print(f'Could not parse telemetry beacon {e}', file = self.file)
            return
        if data:
            print(data, file = self.file)

    @classmethod
    def add_options(cls, parser):
        """
        Adds telemetry parser specific options to the argparse parser
        """
        parser.add_argument('--telemetry_output', default = sys.stdout, help = 'Telemetry output file [default=stdout]')
