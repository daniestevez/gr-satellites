#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital
import pmt

from ... import decode_ra_code
from ...crcs import crc16_arc, crc16_ccitt_false
from ...hier.sync_to_pdu_soft import sync_to_pdu_soft
from ...utils.options_block import options_block


_syncword = {
    'SMOG-P': '0010110111010100',
    'SMOG-1': '001011011101010001100011110001010011010110011001',
    'MRC-100': '11100011000111001001110110101110',
}


fec_sizes = {126: 252, 128: 260, 256: 514}


class mrc100_crc_reorder(gr.basic_block):
    """
    Puts the MRC-100 CRC at the end of the frame.

    The CRC is in bytes 1 and 2 of the frame, and should
    be computed over bytes 0, 3, 4, 5, .... This block rerranges
    the CRC to place it at the end of the frame.
    """
    def __init__(self, inverse=False):
        gr.basic_block.__init__(
            self,
            name='mrc100_crc_reorder',
            in_sig=[],
            out_sig=[])
        self.inverse = False
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        msg = pmt.u8vector_elements(msg)
        if self.inverse:
            msg = msg[:1] + msg[-2:] + msg[1:-2]
        else:
            msg = msg[:1] + msg[3:] + msg[1:3]
        msg = pmt.init_u8vector(len(msg), msg)
        msg_pmt = pmt.cons(pmt.car(msg_pmt), msg)
        self.message_port_pub(pmt.intern('out'), msg_pmt)


class smogp_ra_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the SMOG-P RA FEC frames

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        frame_size: size of the frame before FEC (int)
        variant: variant of the protocol to use ('SMOG-P', 'SMOG-1'
          or 'MRC-100') (str)
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, frame_size, variant='SMOG-P',
                 syncword_threshold=None, options=None):
        gr.hier_block2.__init__(
            self,
            'smogp_ra_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.ra_syncword_threshold
        if syncword_threshold < 0:
            syncword_threshold = self._default_sync_threshold[variant]
        syncword = _syncword[variant]
        self.deframer = sync_to_pdu_soft(
            packlen=fec_sizes[frame_size] * 8, sync=syncword,
            threshold=syncword_threshold)
        self.fec = decode_ra_code(frame_size)
        if variant == 'SMOG-1':
            # CRC-16 ARC
            self.crc = crc16_arc(discard_crc=False)
        elif variant == 'MRC-100':
            self.crc_reorder = mrc100_crc_reorder()
            self.crc = crc16_ccitt_false(
                swap_endianness=True, discard_crc=False)
            self.crc_reorder2 = mrc100_crc_reorder(inverse=True)

        self.connect(self, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.fec, 'in'))
        if variant == 'SMOG-1':
            self.msg_connect((self.fec, 'out'), (self.crc, 'in'))
            self.msg_connect((self.crc, 'ok'), (self, 'out'))
        elif variant == 'MRC-100':
            self.msg_connect((self.fec, 'out'),
                             (self.crc_reorder, 'in'))
            self.msg_connect((self.crc_reorder, 'out'),
                             (self.crc, 'in'))
            self.msg_connect((self.crc, 'ok'),
                             (self.crc_reorder2, 'in'))
            self.msg_connect((self.crc_reorder2, 'out'),
                             (self, 'out'))
        else:
            self.msg_connect((self.fec, 'out'), (self, 'out'))

    _default_sync_threshold = {
        'SMOG-P': 0,
        'SMOG-1': 6,
        'MRC-100': 4,
    }

    @classmethod
    def add_options(cls, parser):
        """
        Adds SMOG-P RA deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--ra_syncword_threshold', type=int,
            default=-1,
            help='RA syncword bit errors [default=%(default)r]')
