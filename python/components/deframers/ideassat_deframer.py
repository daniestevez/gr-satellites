#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital
import pmt
import numpy as np

from ... import nrzi_decode
from ...hier.sync_to_pdu import sync_to_pdu

# the 20 bit syncword is formed by two 0x7e HDLC flags
# encoded as UART with 1 stop bit
_syncword = '00111111010011111101'

class uart_decode(gr.basic_block):
    """
    Helper block to remove UART-like encoding

    The input is unpacked bits having 10 bits per byte consisting of a
    start bit (which should be 0 but we don't look at), an 8-bit byte
    in MSB-first order, and a stop bit (which should be 1 but we don't look at).
    The output consists of the 8-bit bytes as packed bytes.
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="uart_decode",
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = np.array(pmt.u8vector_elements(msg), dtype = 'uint8')
        if packet.size % 10 != 0:
            print("[ERROR] Packet size is not a multiple of 10 bits")
            return
        packet = np.packbits(packet.reshape((-1,10))[:,1:-1])
        packet = bytes(packet) # remove conversion to bytes for GNU Radio 3.9
        self.message_port_pub(pmt.intern('out'),
                              pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet)))


class ideassat_deframer(gr.hier_block2):
    """
    Hierarchical block to deframe IDEASSat ad-hoc UART-like protocol

    The input is a float stream of soft symbols. The output are PDUs
    with IDEASSat frames.

    Args:
        options: Options from argparse
    """
    def __init__(self, options = None):
        gr.hier_block2.__init__(self, "ideassat_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_out('out')

        self.slicer = digital.binary_slicer_fb()
        self.nrzi = nrzi_decode()
        # a length of 40 bytes will give at the end the two 0x7e HDLC flags
        # we do not allow syncword errors because this protocol is very brittle
        self.deframer = sync_to_pdu(packlen = 400,
                                    sync = _syncword,\
                                    threshold = 0)
        self.uart = uart_decode()

        self.connect(self, self.slicer, self.nrzi, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.uart, 'in'))
        self.msg_connect((self.uart, 'out'), (self, 'out'))
