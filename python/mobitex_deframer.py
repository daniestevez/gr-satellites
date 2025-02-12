#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import itertools

from gnuradio import gr
import pmt
import numpy as np

from .check_eseo_crc import crc16_ccitt_zero as crc16_ccitt_zero
from .mobitex_fec import decode, Status


def decode_control_bytes(control_bytes: list[int], control_byte_crc: int):
    # Error Correction of the control bytes
    control_bytes[0], fec0, status0 = decode((control_bytes[0] << 4) | (control_byte_crc >> 4))
    control_bytes[1], fec1, status1 = decode((control_bytes[1] << 4) | (control_byte_crc & 0x0F))
    control_byte_crc = fec0 << 4 | fec1

    # Decode control bytes
    result = {
        'num_data_blocks': (control_bytes[0] & 0x1F) + 1,  # 1st byte, bits 0-4 (+ 1)
        'message_type': (control_bytes[0] >> 5) & 0x07,    # 1st byte, bits 5-7
        'baud_bit': control_bytes[1] & 0x01,               # 2nd byte, bit 0
        'ack_bit': (control_bytes[1] >> 1) & 0x01,         # 2nd byte,bit 1
        'sub_address': (control_bytes[1] >> 2) & 0x03,     # 2nd byte,bits 2-3
        'address': (control_bytes[1] >> 4) & 0x0F,         # 2nd byte,bits 4-7
    }

    if status0 == Status.ERROR_UNCORRECTABLE or status1 == Status.ERROR_UNCORRECTABLE:
        raise ValueError('Control bytes FEC failed.')

    # Count bit errors
    bit_errors = 0
    if  status0 == Status.ERROR_CORRECTED:
        bit_errors += 1
    if  status1 == Status.ERROR_CORRECTED:
        bit_errors += 1

    return result, bit_errors, control_bytes, control_byte_crc


def decode_callsign(callsign_bytes: bytes, crc_bytes: bytes, max_bit_flips: int) -> tuple[bytes, int]:
    """
    Attempt to error-correct a callsign by flipping bits until CRC matches.

    Args:
        callsign_bytes: The callsign bytes to decode
        crc_bytes: The CRC bytes to verify against
        max_bit_flips: Maximum number of bits to flip during error correction

    Returns:
        tuple containing:
            - corrected callsign bytes
            - number of bit errors corrected

    Raises:
        ValueError: If no valid callsign could be found within max_bit_flips bit flips
    """
    # Bit position 0... (N*8); -1 indicates "no flip"
    all_bytes = callsign_bytes + crc_bytes
    flip_positions = range(-1, len(all_bytes) * 8)

    for flips in itertools.combinations(flip_positions, max_bit_flips):
        # Create a modified copy with some bits flipped
        mod_bytes = bytearray(all_bytes)
        for i in flips:
            if i == -1:
                # No flip
                continue
            i_byte = i // 8
            i_bit = i % 8

            # Flip one bit
            mod_bytes[i_byte] = mod_bytes[i_byte] ^ (1 << i_bit)

        # Split back into callsign and CRC
        mod_callsign = mod_bytes[:len(callsign_bytes)]
        mod_crc = mod_bytes[len(callsign_bytes):]

        # Check if modified callsign matches its CRC
        computed_crc = crc16_ccitt_zero(mod_callsign).to_bytes(length=2)

        if computed_crc == bytes(mod_crc):
            callsign_corrected = bytes(mod_callsign)
            bit_errors = sum([1 for x in flips if x != -1])
            return callsign_corrected, bit_errors

    raise ValueError(f'No valid callsign found after flipping up to {max_bit_flips} bits')


def hamming_distance(a: bytes, b: bytes) -> int:
    # Convert bytes to bit arrays
    a_bits = np.unpackbits(np.frombuffer(a, dtype=np.uint8))
    b_bits = np.unpackbits(np.frombuffer(b, dtype=np.uint8))

    # Count differences between bit arrays
    bit_errors = np.count_nonzero(a_bits != b_bits)

    return bit_errors


class mobitex_deframer(gr.basic_block):
    """
    Block to deframe the Mobitex NX protocol.

    # Input
    The input is PDUs with encoded Mobitex-NX frames, _after_ the frame sync and potentially with trailing noise bytes.
        - Control. 2 bytes
        - FEC of control (1 byte, containing 4 parity bits for each control byte)
        - Callsign. 6 bytes in ASCII
        - CRC-16CCITT of Callsign. 2 bytes
        - Multiple Mobitex data blocks. Each Mobitex data block is 30 bytes long

    # Output
    The output is PDUs with Mobitex blocks.
    Each block has the following tags:
        - block_id
    The first block (`block_id`=0) additionally has the following tags:
        - frame_header - the error-corrected frame header
        - control_bit_errors
        - callsign_bit_errors
        - num_blocks

    # Callsign
    If the callsign is known, the deframer will use the hamming-distance between the expected and received callsign & CRC
    to calculte the number of bit errors in the callsign + callsign_crc. This allows correct decoding for frames with many
    bit errors, that otherwise would either have wrongly decoded callsign or dropped would have been dropped due to
    uncorrectable errors.

    # References
    [1]: https://destevez.net/2016/09/some-notes-on-beesat-and-mobitex-nx/
    """
    header_length = 2 + 1 + 6 + 2
    block_size = 30 # (18 message bytes + 2 CRC bytes), encoded with r=12/8 FEC

    def __init__(self, callsign: str=None, callsign_threshold: int=2, verbose=False):
        gr.basic_block.__init__(
            self,
            name='mobitex_deframer',
            in_sig=[],
            out_sig=[])
        self.verbose = verbose
        self.callsign_ref = callsign.encode('ascii') if callsign else None
        self.callsign_threshold = callsign_threshold

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return

        packet = pmt.u8vector_elements(msg)
        control_bytes = packet[:2]
        control_byte_crc = packet[2]
        callsign_bytes = bytes(packet[3:9])
        callsign_crc_bytes = bytes(packet[9:11])

        try:
            control, control_bit_errors, control_corr, control_crc_corr = decode_control_bytes(control_bytes, control_byte_crc)
        except ValueError:
            # Drop frame with uncorrectable bit errors in control bytes
            return

        if self.callsign_ref:
            # Decode known callsign
            callsign_crc_ref = crc16_ccitt_zero(self.callsign_ref).to_bytes(length=2)

            callsign_bit_errors = hamming_distance(
                callsign_bytes + callsign_crc_bytes,
                self.callsign_ref + callsign_crc_ref,
            )
            if callsign_bit_errors > self.callsign_threshold:
                # Drop frame with too many bit errors in callsign
                return
            callsign = self.callsign_ref
        else:
            # Decode unknown callsign
            try:
                callsign, callsign_bit_errors = decode_callsign(
                    callsign_bytes, callsign_crc_bytes, max_bit_flips=self.callsign_threshold)
            except ValueError:
                # Drop frame with uncorrectable bit errors in callsign
                return

        try:
            _ = callsign.decode('ascii')
        except UnicodeDecodeError:
            # Drop frame with non-ASCII callsign
            # (empirically this is always a false-positive syncword match)
            return

        # Apply error-correction to the frame header
        for i in range(2):
            packet[i] = control_corr[i]
        packet[2] = control_crc_corr
        for i in range(6):
            packet[i + 3] = callsign[i]

        frame_header = packet[:self.header_length]
        packet_out = packet[self.header_length:self.header_length + self.block_size * control['num_data_blocks']]

        for block_idx, block in enumerate(itertools.batched(packet_out, n=self.block_size)):
            if block_idx == 0:
                meta = pmt.make_dict()
                meta = pmt.dict_add(
                    meta,
                    pmt.intern('control_bit_errors'),
                    pmt.from_long(control_bit_errors),
                )
                meta = pmt.dict_add(
                    meta,
                    pmt.intern('callsign_bit_errors'),
                    pmt.from_long(callsign_bit_errors),
                )
                meta = pmt.dict_add(
                    meta,
                    pmt.intern('frame_header'),
                    pmt.init_u8vector(len(frame_header), frame_header),
                )
                meta = pmt.dict_add(
                    meta,
                    pmt.intern('num_blocks'),
                    pmt.from_long(control['num_data_blocks']),
                )
            else:
                meta = pmt.make_dict()

            meta = pmt.dict_add(
                meta,
                pmt.intern('block_id'),
                pmt.from_long(block_idx),
            )

            self.message_port_pub(
                pmt.intern('out'),
                pmt.cons(meta, pmt.init_u8vector(len(block), block)))
