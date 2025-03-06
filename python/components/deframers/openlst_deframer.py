#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital
import pmt

from ... import pdu_head_tail
from ...crcs import crc_check
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block


##########################################################################
# The following code is taken from gr-openlst, licensed as
#
# Copyright 2023 Robert Zimmerman.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

aTrellisSourceStateLut = (
    (0, 4), (0, 4), (1, 5), (1, 5), (2, 6), (2, 6), (3, 7), (3, 7),
)
aTrellisTransitionOutput = (
    (0, 3), (3, 0), (1, 2), (2, 1), (3, 0), (0, 3), (2, 1), (1, 2),
)
aTrellisTransitionInput = (0, 1, 0, 1, 0, 1, 0, 1,)


def hamming_weight(byte: int) -> int:
    """Return the number of one bits in a byte"""
    return sum(int(b) for b in f"{byte:b}")


def interleave(chunk: bytes) -> bytes:
    """Interleave or deinterleave a 4 byte chunk"""
    if len(chunk) != 4:
        raise ValueError("interleaving only works on 4 byte chunks")
    chunk_int = int.from_bytes(chunk, byteorder='little')
    grid = []
    for _ in range(4):
        row = []
        for _ in range(4):
            bits = (chunk_int & 0xc0000000) >> 30
            chunk_int = chunk_int << 2
            row.append(bits)
        grid.append(row)

    flipped = 0
    for x in range(4):
        for y in range(4):
            flipped = flipped << 2
            flipped |= grid[y][x]
    return flipped.to_bytes(4, byteorder='little')


def decode_fec_chunk():
    """decode_fec_chunk returns a generator for FEC decode/correction

    This generator decodes FEC + interleaved data per CC1110 DN504 (A).
    This involves deinterleaving and decoding a 2:1 Viterbit sequence.

    The caller passes in 4 byte chunks using the `send` function. The
    generator yields decoded chunks.
    """
    path_bits = 0
    cost = [[100] * 8, [0] * 8]
    path = [[0] * 8, [0] * 8]
    last_buf = 0
    cur_buf = 1
    out = []

    while True:
        chunk = yield bytes(out)
        chunk = interleave(chunk)

        symbols = []
        for b in chunk:
            for _ in range(4):
                symbols.append((b & 0xc0) >> 6)
                b <<= 2
        out = []
        for symbol in symbols:
            # check each state in the trellis
            min_cost = 0xff
            for dest_state in range(8):
                input_bit = aTrellisTransitionInput[dest_state]
                src_state0 = aTrellisSourceStateLut[dest_state][0]
                cost0 = cost[last_buf][src_state0]
                cost0 += hamming_weight(
                    symbol ^ aTrellisTransitionOutput[dest_state][0])
                src_state1 = aTrellisSourceStateLut[dest_state][1]
                cost1 = cost[last_buf][src_state1]
                cost1 += hamming_weight(
                    symbol ^ aTrellisTransitionOutput[dest_state][1])

                if cost0 < cost1:
                    cost[cur_buf][dest_state] = cost0
                    min_cost = min(min_cost, cost0)
                    path[cur_buf][dest_state] = (
                        (path[last_buf][src_state0] << 1) | input_bit)
                else:
                    cost[cur_buf][dest_state] = cost1
                    min_cost = min(min_cost, cost1)
                    path[cur_buf][dest_state] = (
                        (path[last_buf][src_state1] << 1) | input_bit)
            path_bits += 1

            if path_bits >= 32:
                out.append((path[cur_buf][0] >> 24) & 0xff)
                path_bits -= 8
            last_buf = (last_buf + 1) % 2
            cur_buf = (cur_buf + 1) % 2
            for i in range(8):
                cost[last_buf][i] -= min_cost


def pn9():
    """pn9 returns a generator that yields a PN9 sequence

    This can be XORed with a data stream to perform CC1110 whitening
    or dewhitening.
    """
    state = 0b111111111
    while True:
        yield state & 0xff
        for _ in range(8):
            new_bit = ((state & (0x20)) >> 5) ^ (state & 0x01)
            state = (state >> 1) | (new_bit << 8)


def whiten(raw: bytes, gen=None):
    """Whiten/dewhiten data

    If the gen argument is supplied, an existing pn9 generator can
    be used.
    """
    if gen is None:
        gen = pn9()
    return bytes([r ^ p for r, p in zip(raw, gen)])


##########################################################################


class openlst_fec_decode(gr.basic_block):
    """
    Decodes FEC in OpenLST and cuts the the appropriate length
    """
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='openlst_fec_decode',
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
        msg = bytes(pmt.u8vector_elements(msg))

        # FEC decode message beginning to get length field
        chunk0 = msg[:4]
        chunk1 = msg[4:8]
        decoder = decode_fec_chunk()
        decoder.send(None)
        pngen = pn9()
        decoded = whiten(
            decoder.send(msg[:4]) + decoder.send(msg[4:8]),
            pngen)
        length = decoded[0] + 1

        # Decode remaining
        a = 8
        while len(decoded) < length:
            assert len(msg) >= a + 4
            decoded += whiten(decoder.send(msg[a:a+4]), pngen)
            a += 4

        decoded = decoded[:length]
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.car(msg_pmt),
                     pmt.init_u8vector(length, list(decoded))))


_syncword = '11010011100100011101001110010001'


class openlst_deframer(gr.hier_block2, options_block):
    """Hierarchical block to deframe the OpenLST protocol.

    The only configuration currently supported is convolutional coding +
    whitening, as used in the DORA satellite.

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse

    """
    def __init__(self, syncword_threshold=None, options=None):
        gr.hier_block2.__init__(
            self,
            'openlst_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(
            packlen=520, sync=_syncword, threshold=syncword_threshold)
        self.fec = openlst_fec_decode()
        self.crc = crc_check(16, 0x8005, 0xFFFF, 0x0, False, False,
                             True, True)
        # remove header length field (first byte)
        self.crop = pdu_head_tail(3, 1)

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.fec, 'in'))
        self.msg_connect((self.fec, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self, 'out'))

    _default_sync_threshold = 4

    @classmethod
    def add_options(cls, parser):
        """
        Adds OpenLST deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')
