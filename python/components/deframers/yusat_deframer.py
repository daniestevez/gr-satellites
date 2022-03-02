#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021-2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital
import pmt

from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...hdlc_deframer import hdlc_crc_check


# HDLC 0x7e flag
_syncword = '01111110'


class crop_and_check_crc(gr.basic_block):
    """
    Helper block to crop using the final 0x7e flag and check CRC-16
    """
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='crop_and_check_crc',
            in_sig=[],
            out_sig=[])
        self.crc_check = hdlc_crc_check()
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))
        start = 0
        while True:
            idx = packet[start:].find(b'\x7e')
            start += idx + 1
            if idx == -1:
                return
            p = packet[:idx]
            if self.crc_check.fcs_ok(p):
                p = p[:-2]
                self.message_port_pub(
                    pmt.intern('out'),
                    pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(p), p)))
                return


class yusat_deframer(gr.hier_block2):
    """
    Hierarchical block to deframe YUSAT ad-hoc AX.25-like protocol

    The input is a float stream of soft symbols. The output are PDUs
    with YUSAT frames.

    Args:
        options: Options from argparse
    """
    def __init__(self, options=None):
        gr.hier_block2.__init__(
            self,
            'yusat_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_out('out')

        self.slicer = digital.binary_slicer_fb()
        # We hope that 256 bytes is long enough to contain the full packet
        self.deframer = sync_to_pdu_packed(
            packlen=256, sync=_syncword, threshold=0)
        self.crop = crop_and_check_crc()

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self, 'out'))
