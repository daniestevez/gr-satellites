#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Daniel Estevez <daniel@destevez.net>
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy as np
from gnuradio import gr
import pmt

from .snet_telemetry import LTUFrameHeader

from .bch15 import decode_bch15

class snet_deframer(gr.basic_block):
    """
    docstring for block snet_deframer
    """
    def __init__(self, verbose=False):
        gr.basic_block.__init__(self,
            name="snet_deframer",
            in_sig=[],
            out_sig=[])
        self.verbose = verbose

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        bits = np.array(pmt.u8vector_elements(msg))

        ltu = bits[:210].reshape((15,14)).transpose()

        # decode BCH(15,5,7)
        if not all((decode_bch15(ltu[j,:]) for j in range(14))):
            # decode failure
            if self.verbose:
                print('BCH decode failure')
            return
        
        ltu = np.fliplr(ltu[:,-5:]).ravel()
        hdr = LTUFrameHeader.parse(np.packbits(ltu))

        ltu_crc = np.flipud(np.concatenate((ltu[:-5], np.array([1,0,1,1,0,1,1]))).reshape((9,8)))
        # force CRC5 bugs
        ltu_crc[4,:] = ltu_crc[3,:]
        # crc5
        crc = 0x1F
        for bit in ltu_crc.ravel():
            c = crc & 0x10 # check most significant bit in the CRC buffer and safe in a variable.
            c >>= 4 # shift variable to make the compare op. possible (see beneath).
            crc <<= 1 # shift CRC to the left and write 0 into the least significant bit.
            if c != bit:
                crc ^= 0x15 # CRC polynomial
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
            data_bits_per_codeword = 11 # BCH(15,11,3)
            bch_d = 3
        elif hdr.AiTypeSrc == 2:
            data_bits_per_codeword = 7 # BCH(15,7,5)
            bch_d = 5
        elif hdr.AiTypeSrc == 3:
            data_bits_per_codeword = 5 # BCH(15,5,7)
            bch_d = 7
        else:
            if self.verbose:
                print("Invalid AiTypeSrc")
            return

        if uncoded:
            pdu_bytes = np.fliplr(bits[210:210+hdr.PduLength*8].reshape((hdr.PduLength, 8)))
        else:
            data_bytes_per_block = codewords_per_block * data_bits_per_codeword // 8
            num_blocks = int(np.ceil(float(hdr.PduLength) / data_bytes_per_block))

            blocks = list()
            for k in range(num_blocks):
                block = bits[210+k*16*15:210+(k+1)*16*15].reshape((15,16))
                if bch_d:
                    block = block.transpose()

                if not bch_d:
                    print(block)
            
                # decode BCH
                if bch_d and not all((decode_bch15(block[j,:], d = bch_d) for j in range(16))):
                    # decode failure
                    if self.verbose:
                        print('BCH decode failure')
                    return
            
                if bch_d:
                    blocks.append(block[:,-data_bits_per_codeword:].ravel())
                else:
                    blocks.append(block.ravel())

            pdu_bytes = np.fliplr(np.concatenate(blocks).reshape((data_bytes_per_block * num_blocks, 8)))
            pdu_bytes = pdu_bytes[:hdr.PduLength] # drop 0xDB padding bytes at the end
            if not bch_d:
                print(pdu_bytes)

        # crc13
        crc = 0x1FFF
        for bit in np.flipud(pdu_bytes).ravel():
            c = crc & 0x1000 # check most significant bit in the CRC buffer and safe in a variable.
            c >>= 12 # shift variable to make the compare op. possible (see beneath).
            crc <<= 1 # shift CRC to the left and write 0 into the least significant bit.
            if c or bit: # BUG (the correct would be c != bit)
                crc ^= 0x1CF5 # CRC polynomial
            crc &= 0x1FFF

        if crc != hdr.CRC13:
            if self.verbose:
                print('CRC13 fail')
            return

        pdu = bytes(np.packbits(pdu_bytes))
        pdu_tags = pmt.make_dict()
        pdu_tags = pmt.dict_add(pdu_tags, pmt.intern('SNET SrcId'), pmt.from_long(hdr.SrcId))
        self.message_port_pub(pmt.intern('out'),
            pmt.cons(pdu_tags, pmt.init_u8vector(len(pdu), pdu)))
