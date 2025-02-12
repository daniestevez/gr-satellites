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
    control_bytes[0], fec0, status0 = decode(
        (control_bytes[0] << 4) | (control_byte_crc >> 4)
    )
    control_bytes[1], fec1, status1 = decode(
        (control_bytes[1] << 4) | (control_byte_crc & 0x0F)
    )
    control_byte_crc = fec0 << 4 | fec1

    # Decode control bytes
    result = {
        # 1st byte, bits 0-4 (+ 1)
        "num_data_blocks": (control_bytes[0] & 0x1F) + 1,
        # 1st byte, bits 5-7
        "message_type": (control_bytes[0] >> 5) & 0x07,
        # 2nd byte, bit 0
        "baud_bit": control_bytes[1] & 0x01,
        # 2nd byte,bit 1
        "ack_bit": (control_bytes[1] >> 1) & 0x01,
        # 2nd byte,bits 2-3
        "sub_address": (control_bytes[1] >> 2) & 0x03,
        # 2nd byte,bits 4-7
        "address": (control_bytes[1] >> 4) & 0x0F,
    }

    if (
        status0 == Status.ERROR_UNCORRECTABLE or
        status1 == Status.ERROR_UNCORRECTABLE
    ):
        raise ValueError("Control bytes FEC failed.")

    # Count bit errors
    bit_errors = 0
    if status0 == Status.ERROR_CORRECTED:
        bit_errors += 1
    if status1 == Status.ERROR_CORRECTED:
        bit_errors += 1

    return result, bit_errors, control_bytes, control_byte_crc


def decode_unknown_callsign(
    callsign_bytes: bytes,
    crc_bytes: bytes,
    max_bit_flips: int,
    callsign_ref: bytes = None,
) -> tuple[bytes, int]:
    """
    Attempt to error-correct a callsign by flipping bits until CRC matches.

    Args:
        callsign_bytes: The callsign bytes to decode
        crc_bytes: The CRC bytes to verify against
        max_bit_flips: Maximum number of bits to flip during error correction
        callsign_ref: Unused argument

    Returns:
        tuple containing:
            - corrected callsign bytes
            - number of bit errors corrected

    Raises:
        ValueError: If no valid callsign could be found
                    within max_bit_flips bit flips
    """
    if max_bit_flips <= 0:
        # Do not attempt error correction
        computed_crc = crc16_ccitt_zero(bytes(callsign_bytes))
        computed_crc_bytes = computed_crc.to_bytes(length=2)

        if computed_crc_bytes == crc_bytes:
            return callsign_bytes, 0
        else:
            if max_bit_flips == 0:
                raise ValueError('Callsign CRC check failed.')
            else:
                # If max_bit_flips is negative, just accept invalid CRC
                return callsign_bytes, -1

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
        mod_callsign = mod_bytes[: len(callsign_bytes)]
        mod_crc = mod_bytes[len(callsign_bytes):]

        # Check if modified callsign matches its CRC
        computed_crc_bytes = crc16_ccitt_zero(mod_callsign).to_bytes(length=2)

        if computed_crc_bytes == bytes(mod_crc):
            bit_errors = sum([1 for x in flips if x != -1])
            return bytes(mod_callsign), bytes(mod_crc), bit_errors

    raise ValueError(
        f"No valid callsign found after flipping up to {max_bit_flips} bits"
    )


def hamming_distance(a: bytes, b: bytes) -> int:
    # Convert bytes to bit arrays
    a_bits = np.unpackbits(np.frombuffer(a, dtype=np.uint8))
    b_bits = np.unpackbits(np.frombuffer(b, dtype=np.uint8))

    # Count differences between bit arrays
    bit_errors = np.count_nonzero(a_bits != b_bits)

    return bit_errors


def decode_known_callsign(
    callsign_bytes: bytes,
    crc_bytes: bytes,
    max_bit_flips: int,
    callsign_ref: bytes,
) -> tuple[bytes, int]:

    # Decode known callsign
    callsign_crc_ref = crc16_ccitt_zero(callsign_ref).to_bytes(length=2)

    bit_errors = hamming_distance(
        callsign_bytes + crc_bytes,
        callsign_ref + callsign_crc_ref,
    )
    if bit_errors > max_bit_flips:
        # Drop frame with too many bit errors in callsign
        raise ValueError('Callsign invalid, too many bit errors.')

    return callsign_ref, callsign_crc_ref, bit_errors


class mobitex_deframer(gr.basic_block):
    """
    Block to deframe the Mobitex NX protocol.

    # Input
    The input is PDUs with encoded Mobitex-NX frames, _after_ the frame sync
    and potentially with trailing noise bytes.
        - Control. 2 bytes
        - FEC of control (2x 4 parity bits)
        - Callsign. 6 bytes in ASCII
        - CRC-16CCITT of Callsign. 2 bytes
        - Multiple Mobitex data blocks. Each block is 30 bytes

    # Output
    The output is PDUs with Mobitex blocks.
    Each block has the following tags:
        - block_id
    The first block (`block_id`=0) additionally has the following tags:
        - frame_header - the error-corrected frame header
        - control_errors_corrected
        - callsign_bit_errors
        - num_blocks

    # Callsign
    If the callsign is known, the deframer will use the hamming-distance
    between the expected and received callsign & CRC to calculte the number
    of bit errors in the callsign + callsign_crc. This allows correct decoding
    for frames with many bit errors, that otherwise would either have wrongly
    decoded callsign or dropped would have been dropped due to uncorrectable
    errors.

    # References
    [1]: https://destevez.net/2016/09/some-notes-on-beesat-and-mobitex-nx/
    """

    header_length = 2 + 1 + 6 + 2
    bytemap = {
        'control_bytes': slice(0, 2),
        'control_bytes_crc': slice(2, 3),
        'callsign': slice(3, 9),
        'callsign_crc': slice(9, 11),
    }

    # (18 message bytes + 2 CRC bytes), encoded with r=12/8 FEC
    block_size = 30

    def __init__(
        self,
        variant: str,
        callsign: str = None,
        drop_invalid_control: bool = False,
        callsign_threshold: int = 2,
        verbose=False,
    ):
        gr.basic_block.__init__(self,
                                name="mobitex_deframer",
                                in_sig=[],
                                out_sig=[])
        self.verbose = verbose
        self.drop_invalid_control = drop_invalid_control
        self.callsign_ref = callsign.encode("ascii") if callsign else None
        self.callsign_threshold = callsign_threshold

        if variant == 'BEESAT-1':
            self.parse_callsign = False
            self.header_length = 2 + 1
            self.bytemap = {
                'control_bytes': slice(0, 2),
                'control_bytes_crc': slice(2, 3),
            }
        else:
            self.parse_callsign = True

        if variant == 'BEESAT-9':
            self.num_blocks_hardcoded = True
            self.num_blocks = 32
        else:
            self.num_blocks_hardcoded = False

        self.message_port_register_in(pmt.intern("in"))
        self.set_msg_handler(pmt.intern("in"), self.handle_msg)
        self.message_port_register_out(pmt.intern("out"))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return

        packet = pmt.u8vector_elements(msg)

        control_bytes = packet[self.bytemap['control_bytes']]
        control_byte_crc = packet[self.bytemap['control_bytes_crc']][0]

        try:
            control, control_errors_corr, control_corr, control_crc_corr = (
                decode_control_bytes(control_bytes, control_byte_crc)
            )

            # Apply error-correction to the frame header
            for i in range(2):
                packet[i] = control_corr[i]
            packet[2] = control_crc_corr

            control_fec_valid = True
        except ValueError:
            control_errors_corr = 0
            control_fec_valid = False

        if self.drop_invalid_control and not control_fec_valid:
            return

        if self.num_blocks_hardcoded:
            num_blocks = self.num_blocks
        else:
            num_blocks = control['num_data_blocks']

        if self.parse_callsign:
            if self.callsign_ref:
                decode_fn = decode_known_callsign
            else:
                decode_fn = decode_unknown_callsign

            # Decode callsign
            try:
                callsign, callsign_crc, callsign_bit_errors = decode_fn(
                    bytes(packet[self.bytemap['callsign']]),
                    bytes(packet[self.bytemap['callsign_crc']]),
                    max_bit_flips=self.callsign_threshold,
                    callsign_ref=self.callsign_ref,
                )
            except ValueError:
                # Drop frame with either
                # too many uncorrectable bit errors in callsign OR
                # too many detected bit errors compared to expected callsign
                return

            try:
                _ = callsign.decode("ascii")
            except UnicodeDecodeError:
                # Drop frame with non-ASCII callsign
                # (empirically this is always a false-positive syncword match)
                return

            # Apply error-correction
            packet[self.bytemap['callsign']] = callsign[:]
            packet[self.bytemap['callsign_crc']] = callsign_crc[:]
        else:
            # Skip callsign decoding
            pass

        frame_header = packet[: self.header_length]

        blocks_start = self.header_length
        blocks_end = self.header_length + self.block_size * num_blocks
        data_blocks = packet[blocks_start:blocks_end]

        for block_idx, block in enumerate(
            itertools.batched(data_blocks, n=self.block_size)
        ):
            if block_idx == 0:
                meta = pmt.make_dict()
                meta = pmt.dict_add(
                    meta,
                    pmt.intern("control_errors_corrected"),
                    pmt.from_long(control_errors_corr),
                )
                meta = pmt.dict_add(
                    meta,
                    pmt.intern("control_fec_valid"),
                    pmt.from_bool(control_fec_valid),
                )
                if self.parse_callsign:
                    meta = pmt.dict_add(
                        meta,
                        pmt.intern("callsign_bit_errors"),
                        pmt.from_long(callsign_bit_errors),
                    )
                meta = pmt.dict_add(
                    meta,
                    pmt.intern("frame_header"),
                    pmt.init_u8vector(len(frame_header), frame_header),
                )
                meta = pmt.dict_add(
                    meta,
                    pmt.intern("num_blocks"),
                    pmt.from_long(num_blocks),
                )
            else:
                meta = pmt.make_dict()

            meta = pmt.dict_add(
                meta,
                pmt.intern("block_id"),
                pmt.from_long(block_idx),
            )

            self.message_port_pub(
                pmt.intern("out"),
                pmt.cons(meta, pmt.init_u8vector(len(block), block))
            )
