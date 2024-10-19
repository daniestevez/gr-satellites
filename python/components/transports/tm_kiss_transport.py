#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks
import pmt

from ...telemetry.by02 import TMPrimaryHeader as TMPrimaryHeaderShort
from ...telemetry.erminaz import TMPrimaryHeader
from ...kiss import *


class tm_kiss_transport(gr.basic_block):
    """
    Hierarchical block for KISS transport in CCSDS TM packets

    The input are PDUs with TM frames containing a KISS stream.
    The output are PDUs with the packets encapsulated in the stream.

    Args:
        virtual_channels: List of virtual channels to extract
        short_tm: Use short TM header from BY02 and other missions
        options: Command line options (ignored)
    """
    def __init__(self, virtual_channels=[], short_tm=False, options=None):
        gr.basic_block.__init__(
            self,
            name='tm_kiss_transport',
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))
        self.packets = {vc: [] for vc in virtual_channels}
        self.transpose = {vc: False for vc in virtual_channels}
        self.tm_header = (
            TMPrimaryHeaderShort if short_tm else TMPrimaryHeader)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        frame = bytes(pmt.u8vector_elements(msg))
        if len(frame) <= self.tm_header.sizeof():
            return
        header = self.tm_header.parse(frame)
        vc = header.virtual_channel_id
        try:
            packet = self.packets[vc]
        except KeyError:
            return
        payload = frame[self.tm_header.sizeof():]
        for c in payload:
            if c == FEND:
                if len(packet) > 0:
                    self.message_port_pub(
                        pmt.intern('out'),
                        pmt.cons(pmt.PMT_NIL,
                                 pmt.init_u8vector(len(packet), packet)))
                    self.packets[vc] = []
            elif self.transpose[vc]:
                if c == TFEND:
                    packet.append(FEND)
                elif c == TFESC:
                    packet.append(FESC)
                self.transpose[vc] = False
            elif c == FESC:
                self.transpose[vc] = True
            else:
                packet.append(c)
