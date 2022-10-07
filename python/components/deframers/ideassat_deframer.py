#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import struct

from gnuradio import gr, digital
import numpy as np
import pmt

from ... import crc, nrzi_decode
from ...hier.sync_to_pdu import sync_to_pdu
from ...utils.options_block import options_block


# The 40 bit syncword is formed by 4130f000, which is the end of the
# AX.25 address of the first subpacket (including the subpacket counter),
# encoded as UART with 1 stop bit.
_syncword = '0010000011000110000101111000010000000001'


class uart_decode(gr.basic_block):
    """
    Helper block to remove UART-like encoding

    The input is unpacked bits having 10 bits per byte consisting of a
    start bit (which should be 0 but we don't look at), an 8-bit byte
    in MSB-first order, and a stop bit (which should be 1 but we don't
    look at). The output consists of the 8-bit bytes as packed bytes.
    """
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='uart_decode',
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = np.array(pmt.u8vector_elements(msg), dtype='uint8')
        if packet.size % 10 != 0:
            print('[ERROR] Packet size is not a multiple of 10 bits')
            return
        packet = np.packbits(packet.reshape((-1, 10))[:, 1:-1])
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet)))


class extract_payload(gr.basic_block):
    """
    Helper block to throw subpacket headers and extract CRC-protected payload

    This also checks the CRC
    """
    def __init__(self, verbose=False):
        gr.basic_block.__init__(
            self,
            name='extract_payload',
            in_sig=[],
            out_sig=[])
        self.crc_calc = crc(16, 0x1021, 0xFFFF, 0x0, False, False)
        self.verbose = verbose
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = np.array(pmt.u8vector_elements(msg), dtype='uint8')
        # Put initial padding to account for the AX.25 header we've lost
        initial_padding = np.zeros(17, dtype='uint8')
        packet = np.concatenate((initial_padding, packet))
        if packet.size != 40 * 9:
            print('[ERROR] Invalid packet size')
            return
        packet = packet.reshape((9, 40))
        # Save AX.25 header. we take it from the 2nd message
        header = packet[1, 1:16]
        # Drop AX.25 headers and final 0x7e
        packet = packet[:, 17:-1].ravel()
        # Drop final padding
        packet = packet[:-11]
        # Check CRC (do not include first 4 bytes)
        crc_val = self.crc_calc.compute(packet[4:-2])
        if crc_val != struct.unpack('<H', packet[-2:])[0]:
            if self.verbose:
                print('CRC failed')
                return
        elif self.verbose:
            print('CRC OK')
        # Drop CRC
        packet = packet[:-2]
        # Put AX.25 header back
        packet = np.concatenate((header, packet))
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet)))


class ideassat_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe IDEASSat ad-hoc UART-like protocol

    The input is a float stream of soft symbols. The output are PDUs
    with IDEASSat frames.

    Args:
        options: Options from argparse
    """
    def __init__(self, options=None):
        gr.hier_block2.__init__(
            self,
            'ideassat_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        self.slicer = digital.binary_slicer_fb()
        self.nrzi = nrzi_decode()
        # A length of 40 bytes will give at the end the two 0x7e HDLC flags
        # we do not allow syncword errors because this protocol is very
        # brittle.
        self.deframer = sync_to_pdu(
            packlen=10 * (9*40 - 17), sync=_syncword, threshold=0)
        self.uart = uart_decode()
        self.payload = extract_payload(self.options.verbose_crc)

        self.connect(self, self.slicer, self.nrzi, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.uart, 'in'))
        self.msg_connect((self.uart, 'out'), (self.payload, 'in'))
        self.msg_connect((self.payload, 'out'), (self, 'out'))

    @classmethod
    def add_options(cls, parser):
        """
        Adds IDEASSat deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--verbose_crc', action='store_true', help='Verbose CRC')
