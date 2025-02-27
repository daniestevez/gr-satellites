# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later

import itertools

from gnuradio import gr
import numpy as np
import pmt

from .check_eseo_crc import crc16_ccitt_zero as crc16_ccitt_zero
from .mobitex_fec import decode, Status

DEBUG = False

class mobitex_fec(gr.basic_block):
    """
    Block to perform error-correction on Mobitex data blocks.

    # Input
    PDU with one encoded Mobitex data block (20 * 12 bits)

    # Output
    PDU with one decoded Mobitex data block (20 * 8 bits)
    Tags:
        - block_bit_errors (int): Number of corrected bit errors
        - block_fec_failed (bool): True if one or more words could not be correctly decoded
    """

    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='mobitex_fec',
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        meta = pmt.car(msg_pmt)
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return

        block = pmt.u8vector_elements(msg)

        if len(block) != 30:
            print(
                '[ERROR] Received invalid Mobitex data block, '
                f'expected 30 bytes (got {len(block)} bytes).'
            )
            return

        # Extract individual bits
        bits = np.zeros((240,), dtype=np.uint8)
        for i in range(len(block)):
            # Convert each byte to its 8 individual bits
            bits_in_byte = np.array(list(map(int, format(block[i], '08b'))))
            # Store in output_bits array
            bits[i*8:(i+1)*8] = bits_in_byte

        if DEBUG:
            print('\nError-corrected data block:')

        packet_out = []
        bit_errors = 0
        fec_failed = False
        for word_idx, codeword_bits in enumerate(itertools.batched(bits, n=12)):
            # Convert codeword bits to 12-bit codeword (packed in 2 bytes)
            bits_str = ''.join([str(x) for x in codeword_bits])
            codeword_int = int(bits_str, 2)
            codeword = codeword_int.to_bytes(2, byteorder='big')

            corrected, _, status = decode(codeword_int)
            packet_out.append(corrected)

            if DEBUG:
                row = bits[word_idx * 12:(word_idx + 1) * 12]
                bits_str = ''.join(['1' if b else '0' for b in row])

                print(f'{bits_str} | {codeword.hex()[1:].upper()} | {status}')

            if status == Status.NO_ERROR:
                pass
            elif status == Status.ERROR_CORRECTED:
                bit_errors += 1
            elif status == Status.ERROR_UNCORRECTABLE:
                fec_failed = True

        meta = pmt.dict_add(
            meta,
            pmt.intern('block_bit_errors'),
            pmt.from_long(bit_errors),
        )
        meta = pmt.dict_add(
            meta,
            pmt.intern('block_fec_failed'),
            pmt.from_bool(fec_failed),
        )
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(meta, pmt.init_u8vector(len(packet_out), packet_out)))
