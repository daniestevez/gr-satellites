#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2023 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks
import numpy as np
import pmt

from ...crcs import crc16_ccitt_zero


class nanolink_defragmenter(gr.basic_block):
    """
    NANOLINK defragmenter.

    The input are PDUs with a NANOLINK byte-stream. The output are PDUs
    with the NANOLINK frames encapsulated in the stream.

    Args:
        options: options from argparse
    """

    def __init__(self, options=None):
        gr.basic_block.__init__(
            self,
            name='nanolink_defragmenter',
            in_sig=None,
            out_sig=None)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))
        self.in_frame = False

    def handle_msg(self, msg_pmt):
        meta = pmt.car(msg_pmt)
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            return

        in0 = bytes(pmt.u8vector_elements(msg))
        syncword = bytes.fromhex('faf320')
        header_len = 3
        while in0:
            if not self.in_frame:
                a = in0.find(syncword)
                if a == -1:
                    # syncword doesn't appear in input
                    return
                self.in_frame = True
                self.remain = None
                header = in0[a+len(syncword):a+len(syncword)+header_len]
                in0 = in0[a+len(syncword)+header_len:]
                self.current = header
            # here self.in_frame == True
            if len(self.current) < header_len:
                missing = header_len - len(self.current)
                self.current += in0[:missing]
                in0 = in0[missing:]
                if len(self.current) < header_len:
                    # still we don't have a full header
                    return
            if self.remain is None:
                header = self.current
                seq = header[0]
                vc = (header[2] >> 1) & 0x7
                length = ((header[1] & 0x3f) << 4) | (header[2] >> 4)
                arq = header[1] >> 7
                ext = (header[1] >> 6) & 1
                self.remain = length
            b = self.remain
            self.current += in0[:b]
            self.remain -= len(in0[:b])
            in0 = in0[b:]
            if self.remain == 0:
                self.in_frame = False
                self.remain = None
                self.message_port_pub(
                    pmt.intern('out'),
                    pmt.cons(pmt.PMT_NIL,
                             pmt.init_u8vector(len(self.current),
                                               list(self.current))))


class nanolink_transport(gr.hier_block2):
    """
    Hierarchical block for NANOLINK transport.

    The input are PDUs with a NANOLINK byte-stream. The output are PDUs
    with the NANOLINK frames encapsulated in the stream.

    Args:
        options: options from argparse
    """
    def __init__(self, options=None):
        gr.hier_block2.__init__(
            self,
            'nanolink_transport',
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_in('in')
        self.message_port_register_hier_out('out')

        self.nanolink = nanolink_defragmenter()
        self.crc_check = crc16_ccitt_zero()

        self.msg_connect((self, 'in'), (self.nanolink, 'in'))
        self.msg_connect((self.nanolink, 'out'), (self.crc_check, 'in'))
        self.msg_connect((self.crc_check, 'ok'), (self, 'out'))
