#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018,2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import numpy as np
import pmt

from .bch15 import decode_bch15
from .telemetry.snet import LTUFrameHeader


class snet_deframer(gr.basic_block):
    """docstring for block snet_deframer"""
    def __init__(self, verbose=False, buggy_crc=True):
        gr.basic_block.__init__(
            self,
            name='snet_deframer',
            in_sig=[],
            out_sig=[])
        self.verbose = verbose
        self.buggy_crc = buggy_crc

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        bits = np.array(pmt.u8vector_elements(msg))

        ltu = bits[:210].reshape((15, 14)).transpose()

        # Decode BCH(15,5,7)
        if not all((decode_bch15(ltu[j, :]) for j in range(14))):
            # Decode failure
            if self.verbose:
                print('BCH decode failure')
            return

        ltu = np.fliplr(ltu[:, -5:]).ravel()
        hdr = LTUFrameHeader.parse(np.packbits(ltu))

        ltu_crc = np.concatenate((ltu[:-5], np.array([1, 0, 1, 1, 0, 1, 1])))
        ltu_crc = ltu_crc.reshape((9, 8))
        if self.buggy_crc:
            # Reverse byte ordering for CRC5 calculation
            ltu_crc = np.flipud(ltu_crc)

        if self.buggy_crc:
            # Force CRC5 bugs
            ltu_crc[4, :] = ltu_crc[3, :]
        # CRC5 calculation
        crc = 0x1F
        for bit in ltu_crc.ravel():
            # Check most significant bit in the CRC buffer and save
            # in a variable.
            c = crc & 0x10
            # Shift variable to make the compare op. possible (see beneath).
            c >>= 4
            # Shift CRC to the left and write 0 into the least significant bit.
            crc <<= 1
            if c != bit:
                crc ^= 0x15  # CRC polynomial
            crc &= 0x1F

        if crc != hdr.CRC5:
            if self.verbose:
                print('CRC5 fail')
            return

        if self.verbose:
            print(hdr)

        if hdr.PduLength == 0:
            return

        codewords_per_block = 16
        uncoded = False
        if hdr.AiTypeSrc == 0:
            uncoded = True
        elif hdr.AiTypeSrc == 1:
            data_bits_per_codeword = 11  # BCH(15,11,3)
            bch_d = 3
        elif hdr.AiTypeSrc == 2:
            data_bits_per_codeword = 7  # BCH(15,7,5)
            bch_d = 5
        elif hdr.AiTypeSrc == 3:
            data_bits_per_codeword = 5  # BCH(15,5,7)
            bch_d = 7
        else:
            if self.verbose:
                print('Invalid AiTypeSrc')
            return

        if uncoded:
            pdu_bytes = bits[210:210+hdr.PduLength*8]
            pdu_bytes = pdu_bytes.reshape((hdr.PduLength, 8))
            pdu_bytes = np.fliplr(pdu_bytes)
        else:
            data_bytes_per_block = (codewords_per_block
                                    * data_bits_per_codeword // 8)
            num_blocks = int(np.ceil(float(
                hdr.PduLength) / data_bytes_per_block))

            blocks = list()
            for k in range(num_blocks):
                block = bits[210+k*16*15:210+(k+1)*16*15].reshape((15, 16))
                if bch_d:
                    block = block.transpose()

                if not bch_d:
                    print(block)

                # Decode BCH
                if (bch_d
                        and not all((decode_bch15(block[j, :], d=bch_d)
                                     for j in range(16)))):
                    # Decode failure
                    if self.verbose:
                        print('BCH decode failure')
                    return

                if bch_d:
                    blocks.append(block[:, -data_bits_per_codeword:].ravel())
                else:
                    blocks.append(block.ravel())

            pdu_bytes = np.concatenate(blocks)
            pdu_bytes = pdu_bytes.reshape((data_bytes_per_block
                                           * num_blocks, 8))
            pdu_bytes = np.fliplr(pdu_bytes)
            # Drop 0xDB padding bytes at the end
            pdu_bytes = pdu_bytes[:hdr.PduLength]
            if not bch_d:
                print(pdu_bytes)

        # CRC13
        crc = 0x1FFF
        pdu_crc = np.flipud(pdu_bytes) if self.buggy_crc else pdu_bytes
        for bit in pdu_crc.ravel():
            # Check most significant bit in the CRC buffer and save it
            # in a variable.
            c = crc & 0x1000
            # Shift variable to make the compare op. possible (see beneath).
            c >>= 12
            # Shift CRC to the left and write 0 into the least significant bit.
            crc <<= 1
            if (c or bit if self.buggy_crc else c != bit):
                crc ^= 0x1CF5  # CRC polynomial
            crc &= 0x1FFF

        if crc != hdr.CRC13:
            if self.verbose:
                print('CRC13 fail')
            return

        pdu = np.packbits(pdu_bytes)
        pdu_tags = pmt.make_dict()
        pdu_tags = pmt.dict_add(
            pdu_tags, pmt.intern('SNET SrcId'), pmt.from_long(hdr.SrcId))
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pdu_tags, pmt.init_u8vector(len(pdu), pdu)))
