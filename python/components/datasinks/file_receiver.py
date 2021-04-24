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

from ... import filereceiver


class file_receiver(gr.basic_block):
    """
    Block for file reception

    The input are PDUs with frames

    The frames are expected to contain file chunks, which are saved
    into files using a FileReceiver object.

    Args:
        receiver: FileReceiver object (to load from the
            filereceiver package) (str)
        path: path to save files to (str)
        verbose: use verbose messages in FileReceiver (bool)
        options: options from argparse
        **kwargs: these are passed straight to the FileReceiver object
    """
    def __init__(self, receiver, path=None, verbose=None,
                 options=None, **kwargs):
        gr.basic_block.__init__(
            self,
            'file_receiver',
            in_sig=[],
            out_sig=[])
        if verbose is None:
            if options is not None:
                verbose = options.verbose_file_receiver
            else:
                raise ValueError(
                    'Must indicate verbose in function arguments or options')
        if path is None:
            if options is not None:
                path = options.file_output_path
            else:
                raise ValueError(
                    'Must indicate path in function arguments or options')
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.receiver = getattr(filereceiver, receiver)(path,
                                                        verbose, **kwargs)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))

        self.receiver.push_chunk(packet)

    @classmethod
    def add_options(cls, parser):
        """
        Adds telemetry parser specific options to the argparse parser
        """
        parser.add_argument(
            '--file_output_path', default='/tmp',
            help='File output path [default=%(default)r]')
        parser.add_argument(
            '--verbose_file_receiver',
            action='store_true',
            help='Verbose file receiver')
