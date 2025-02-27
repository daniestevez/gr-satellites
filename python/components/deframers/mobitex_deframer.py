#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 - 2025 Daniel Estevez <daniel@destevez.net>, Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import importlib

from gnuradio import gr, blocks, digital

from ... import mobitex_deframer as deframer
from ...mobitex_fec_block import mobitex_fec
from ...mobitex_scrambler import mobitex_scrambler_bb
from ...tubix20_reframer import tubix20_reframer
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block
from ...grtypes import byte_t
from ...grpdu import pdu_to_tagged_stream, tagged_stream_to_pdu


class mobitex_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe Mobitex and Mobitex-NX

    The input are PDUs.
    The output are PDUs with Mobitex-NX frames.


    This uses either
    - the gr-tnc_nx OOT module (only attempts to import it when __init__() is called)
    - the builitin mobitex deframer

    # builtin mobitex deframer specific comments
    If the callsign is provided, the deframer can detect otherwise uncorrectable bit errors sometimes.
    unknown callsign - recommended callsign_threshold is 8
    known callsign -   recommended callsign_threshold is 12

    Args:
        nx: use NX mode (boolean)
        callsign: Expected callign (optional).
        syncword_threshold: number of bit errors allowed in syncword (int)
        syncword_threshold: number of bit errors allowed in callsign + callsign crc (int)
        options: Options from argparse
    """
    default_syncword = 0x5765
    default_nx_syncword = 0x0EF0

    _default_sync_threshold = 3      # accept <= 3 bit errors in 2 bytes payload, 2x 4-bit FEC)
    _default_callsign_threshold = 2  # accept <= 2 bit errors in 6 bytes payload, 1x16-bit CRC)

    # 2 bytes - control bytes
    # 1 byte - FEC of control
    # 6 bytes - callsign
    # 2 bytes - CRC-16CCITT of Callsign
    header_length = 2 + 1 + 6 + 2

    # (18 bytes + 2 bytes CRC) * r=12/8 (FEC) = 30 bytes
    block_length_encoded = 30

    # Maximum number of Mobitex blocks per frame
    max_blocks = 32

    use_scrambler = True
    use_interleaver = True
    use_fec = True

    def __init__(self, nx=False, callsign=None, callsign_threshold=None, syncword_threshold=None, options=None):
        gr.hier_block2.__init__(
            self,
            'mobitex_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        self.message_port_register_hier_out('out')

        self.nx = nx
        self.syncword = self.default_nx_syncword if self.nx else self.default_syncword
        self.callsign = callsign

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold
        self.syncword_threshold = syncword_threshold

        if callsign_threshold is None:
            callsign_threshold = self.options.callsign_threshold
        self.callsign_threshold = callsign_threshold

        self.invert = blocks.multiply_const_ff(-1, 1)
        self.slicer = digital.binary_slicer_fb()

        if self.options.use_tnc_nx:
            self.setup_external_deframer()
        else:
            self.setup_builtin_deframer()

    def setup_external_deframer(self):
        try:
            tnc_nx = importlib.import_module('tnc_nx')
        except ImportError as e:
            print('Unable to import tnc_nx')
            print('gr-tnc_nx needs to be installed to use Mobitex')
            raise e
        self.mobitex = tnc_nx.nx_decoder(self.syncword, self.nx)
        self.connect(self, self.invert, self.slicer, self.mobitex)
        self.msg_connect((self.mobitex, 'out'), (self, 'out'))

    def setup_builtin_deframer(self):
        # Setup blocks
        self.sync2pdu = sync_to_pdu_packed(
            packlen=self.header_length + self.block_length_encoded * self.max_blocks,
            sync=f'{self.syncword:016b}',
            threshold=self.syncword_threshold
        )
        self.crop = deframer(
            callsign=self.callsign,
            callsign_threshold=self.callsign_threshold
        )
        self.pdu2stream = pdu_to_tagged_stream(byte_t, 'packet_len')
        self.unpack = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.interleaver = blocks.matrix_interleaver(
            itemsize=1, rows=12,
            cols=20, deint=False,
        )
        self.scrambler = mobitex_scrambler_bb()
        self.pack = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.stream2pdu = tagged_stream_to_pdu(byte_t, 'packet_len')
        self.fec = mobitex_fec()

        self.reframer = tubix20_reframer()

        # Setup connections
        self.connect(self, self.invert, self.slicer, self.sync2pdu)
        self.msg_connect((self.sync2pdu, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.pdu2stream, 'pdus'))

        my_blocks = [self.pdu2stream, self.unpack]

        if self.use_scrambler:
            my_blocks.append(self.scrambler)
        if self.use_interleaver:
            my_blocks.append(self.interleaver)

        my_blocks.append(self.pack)
        my_blocks.append(self.stream2pdu)

        self.connect(*my_blocks)

        self.msg_connect((self.stream2pdu, 'pdus'), (self.fec, 'in'))
        self.msg_connect((self.fec, 'out'), (self.reframer, 'in'))
        self.msg_connect((self.reframer, 'out'), (self, 'out'))

    @classmethod
    def add_options(cls, parser):
        """
        Adds Mobitex deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')
        parser.add_argument(
            '--callsign_threshold', type=int,
            default=cls._default_callsign_threshold,
            help='Callsign & callsign CRC bit errors [default=%(default)r]')
        parser.add_argument(
            '--use_tnc_nx', type=bool,
            default=False,
            help='Use gr-tnc_nx OOT module instead of builtin de-framer')
