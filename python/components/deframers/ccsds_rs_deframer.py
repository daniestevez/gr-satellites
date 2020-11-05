#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital
from ... import decode_rs
from ...hier.sync_to_pdu import sync_to_pdu
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...hier.ccsds_descrambler import ccsds_descrambler
from ...utils.options_block import options_block

_syncword = '00011010110011111111110000011101'

class ccsds_rs_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe CCSDS Reed-Solomon TM frames

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        frame_size: frame size (not including parity check bytes) (int)
        precoding: either None or 'differential' for differential precoding (str)
        rs_basis: Reed-Solomon basis, either 'conventional' or 'dual' (str)
        rs_interleaving: Reed-Solomon interleaving depth (int)
        scrambler: scrambler to use, either 'CCSDS' or 'none' (str)
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, frame_size = 223, precoding = None, rs_basis = 'dual',
                     rs_interleaving = 1, scrambler = 'CCSDS',
                     syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "ccsds_rs_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        if precoding not in [None, 'differential']:
            raise ValueError(f'invalid precoding {precoding}')
        if rs_basis not in ['conventional', 'dual']:
            raise ValueError(f'invalid Reed-Solomon basis {rs_basis}')
        if scrambler not in ['CCSDS', 'none']:
            raise ValueError(f'invalid scrambler {scrambler}')
        
        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        if precoding == 'differential':
            self.differential = digital.diff_decoder_bb(2)
        deframe_func = sync_to_pdu if scrambler == 'CCSDS' else sync_to_pdu_packed
        packlen_mult = 8 if scrambler == 'CCSDS' else 1
        self.deframer = deframe_func(packlen = (frame_size + 32) * packlen_mult,
                                        sync = _syncword,
                                        threshold = syncword_threshold)
        if scrambler == 'CCSDS':
            self.scrambler = ccsds_descrambler()
        self.fec = decode_rs(rs_basis == 'dual', rs_interleaving)

        self._blocks = [self, self.slicer]
        if precoding == 'differential':
            self._blocks.append(self.differential)
        self._blocks += [self.deframer]

        self.connect(*self._blocks)
        if scrambler == 'CCSDS':
            self.msg_connect((self.deframer, 'out'), (self.scrambler, 'in'))
            self.msg_connect((self.scrambler, 'out'), (self.fec, 'in'))
        else:
            self.msg_connect((self.deframer, 'out'), (self.fec, 'in'))
        self.msg_connect((self.fec, 'out'), (self, 'out'))

    _default_sync_threshold = 4
        
    @classmethod
    def add_options(cls, parser):
        """
        Adds CCSDS RS deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
        parser.add_argument('--verbose_rs', action = 'store_true', help = 'Verbose RS decoder')
