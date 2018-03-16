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
import array

from snet_telemetry import LTUFrameHeader

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
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        #packet = bytearray(pmt.u8vector_elements(msg))
        bits = np.array(pmt.u8vector_elements(msg))

        ltu = bits[:210].reshape((15,14)).transpose()
        # TODO decode BCH(15,5,7)
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
                print 'CRC5 fail'
            return

        if self.verbose:
            print(hdr)
            
        if hdr.PduLength == 0:
            return
        
        codewords_per_block = 16
        if hdr.AiTypeSrc == 0:
            data_bits_per_codeword = 15 # uncoded
        elif hdr.AiTypeSrc == 1:
            data_bits_per_codeword = 11 # BCH(15,11,3)
        elif hdr.AiTypeSrc == 2:
            data_bits_per_codeword = 7 # BCH(15,7,5)
        elif hdr.AiTypeSrc == 3:
            data_bits_per_codeword = 5 # BCH(15,5,7)
        else:
            if self.verbose:
                print "Invalid AiTypeSrc"
            return

        data_bytes_per_block = codewords_per_block * data_bits_per_codeword // 8
        num_blocks = int(np.ceil(float(hdr.PduLength) / data_bytes_per_block))

        blocks = list()
        for k in range(num_blocks):
            block = bits[210+k*16*15:210+(k+1)*16*15].reshape((15,16)).transpose()
            # TODO decode BCH
            blocks.append(block[:,-data_bits_per_codeword:].ravel())

        pdu_bytes = np.fliplr(np.concatenate(blocks).reshape((data_bytes_per_block * num_blocks, 8)))
        pdu_bytes = pdu_bytes[:hdr.PduLength] # drop 0xDB padding bytes at the end

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

        pdu = array.array('B', np.packbits(pdu_bytes))
        self.message_port_pub(pmt.intern('out'),
            pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(pdu), pdu)))
