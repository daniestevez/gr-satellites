#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, digital
import pmt
import numpy as np

from ... import viterbi_decoder
from ...hdlc_deframer import hdlc_deframer
from ...hier.sync_to_pdu import sync_to_pdu
from ...utils.options_block import options_block
from ...check_tt64_crc import crc_table

# two HDLC flags encoded and interleaved (32 bits)
_syncword = '10001010111001101000101011100110'

class deinterleave(gr.basic_block):
    """
    Helper block to perform 4x4 matrix deinterleaving

    The input and output are PDUs with unpacked bits
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="deinterleave",
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
        if packet.size % 16 != 0:
            print("[ERROR] Packet size is not a multiple of 16 bits")
            return
        packet = np.einsum('ijk->ikj', packet.reshape((-1,4,4))).ravel()
        # invert every other bit, since the g0 branch of the convolutional
        # encoder is inverted
        packet[::2] ^= 1
        self.message_port_pub(pmt.intern('out'),
                              pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet)))

def crc16_usb(data):
    crc = 0xffff
    for byte in data:
        tbl_idx = (crc ^ byte) & 0xff
        crc = (crc_table[tbl_idx] ^ (crc >> 8)) & 0xffff
    return (crc ^ 0xffff) & 0xffff
        
def crc_check(frame):
    if len(frame) <= 2: return False
    crc = crc16_usb(frame[:-2])
    return frame[-2] == (crc & 0xff) and frame[-1] == ((crc >> 8) & 0xff)
        
class ax5043_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe AX5043 FEC packets

    The input is a float stream of soft symbols. The output are PDUs
    with the FEC frames. The AX5043 uses a k = 5, r = 1/2 convolutional
    code, 4x4 matrix interleaving, and HDLC framing. This deframer uses
    a Viterbi decoder that works on hard-decision bits.

    Args:
        options: Options from argparse
    """
    def __init__(self, options = None):
        gr.hier_block2.__init__(self, "ax5043_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        self.slicer = digital.binary_slicer_fb()
        # 4000 bits will leave enough room for the 200 byte packets
        self.deframer = sync_to_pdu(packlen = 4000,
                                    sync = _syncword,\
                                    threshold = 4)
        self.deinterleave = deinterleave()
        self.viterbi = viterbi_decoder(5, [25, 23])
        self.pdu2tag = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.hdlc = hdlc_deframer(True, 10000, crc_check_func = crc_check)

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.deinterleave, 'in'))
        self.msg_connect((self.deinterleave, 'out'), (self.viterbi, 'in'))
        self.msg_connect((self.viterbi, 'out'), (self.pdu2tag, 'pdus'))
        self.connect(self.pdu2tag, self.hdlc)
        self.msg_connect((self.hdlc, 'out'), (self, 'out'))

    @classmethod
    def add_options(cls, parser):
        """
        Adds AX5043 deframer specific options to the argparse parser
        """
        parser.add_argument('--verbose_crc', action = 'store_true', help = 'Verbose CRC')
