#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from typing import List, Optional, Tuple

import itertools

from gnuradio import gr

import pmt
import numpy as np

from .check_eseo_crc import crc16_ccitt_zero as crc16_ccitt_zero
from .mobitex_fec import decode, encode, Status


def decode_control(control0: int, control1: int, fec: int) -> \
        Optional[Tuple[List[int], int]]:
    """
    Process control bytes and FEC byte, correcting errors if possible.
    Returns error-corrected bytes and error count, or None if uncorrectable.
    """
    # Error Correction of the control bytes
    control0, fec0, status0 = decode(
        (control0 << 4) | (fec >> 4)
    )
    control1, fec1, status1 = decode(
        (control1 << 4) | (fec & 0x0F)
    )
    fec = fec0 << 4 | fec1

    if status0 == Status.ERROR_UNCORRECTABLE or \
            status1 == Status.ERROR_UNCORRECTABLE:
        # Check of control bytes FEC failed
        return None

    # Count bit errors
    bit_errors = sum(s == Status.ERROR_CORRECTED for s in (status0, status1))

    return [control0, control1, fec], bit_errors


def encode_control(control0: int, control1: int) -> int:
    """
    Generate FEC byte from pair of control bytes.
    Returns computed FEC byte.
    """
    fec0 = encode(control0) & 0xf
    fec1 = encode(control1) & 0xf
    fec = fec0 << 4 | fec1

    return fec


def check_callsign_crc(callsign: bytes, crc: bytes):
    computed_crc = crc16_ccitt_zero(
        callsign).to_bytes(length=2, byteorder='big')

    return computed_crc == crc


def decode_unknown_callsign(
    callsign: bytes,
    crc: bytes,
    max_bit_flips: int,
) -> Optional[Tuple[bytes, bytes, int]]:
    """Error-corrects callsign+crc by flipping bits until CRC matches or
    maximum number of bit-flips is exceeded.

    Returns:
        (corrected_callsign, corrected_crc, num_bit_errors)
        or
        None, if number of bit-flips is exceeded.
    """
    for num_flips in range(max_bit_flips + 1):
        flip_positions = range(len(callsign + crc) * 8)
        for flips in itertools.combinations(flip_positions, num_flips):
            # Perform flips indicated by the pattern
            mod_bytes = bytearray(callsign + crc)
            for i in flips:
                # Flip a single bit
                i_byte = i // 8
                i_bit = i % 8
                mod_bytes[i_byte] = mod_bytes[i_byte] ^ (1 << i_bit)

            # Split back into callsign and CRC
            mod_callsign = bytes(mod_bytes[: len(callsign)])
            mod_crc = bytes(mod_bytes[len(callsign):])

            # Check CRC
            if not check_callsign_crc(mod_callsign, mod_crc):
                continue

            # Valid solution found, exit early.
            bit_errors = sum([1 for x in flips if x != -1])
            return mod_callsign, mod_crc, bit_errors

    # No valid callsign found, within given maximum number of bit flips
    return None


def hamming_distance(a: bytes, b: bytes) -> int:
    # Convert bytes to bit arrays
    a_bits = np.unpackbits(np.frombuffer(a, dtype=np.uint8))
    b_bits = np.unpackbits(np.frombuffer(b, dtype=np.uint8))

    # Count differences between bit arrays
    bit_errors = np.count_nonzero(a_bits != b_bits)

    return bit_errors


def compare_expected_callsign(
    callsign: bytes,
    crc: bytes,
    callsign_ref: bytes,
) -> Tuple[bytes, int]:
    """
    Calculates bit errors between received callsign+CRC and expected
    reference callsign+CRC.

    Returns:
        reference callsign CRC along with number of bit errors.
    """
    crc_ref = crc16_ccitt_zero(
        callsign_ref).to_bytes(length=2, byteorder='big')

    bit_errors = hamming_distance(
        callsign + crc,
        callsign_ref + crc_ref,
    )

    return crc_ref, bit_errors


class mobitex_to_datablocks(gr.basic_block):
    """
    Block to deframe the Mobitex NX protocol.

    ## Input
    Input is PDUs with one encoded Mobitex-NX frame per PDU.

    The block usually comes as the first block after the frame sync was done.
    This block decodes the control bytes to receive the number of data blocks,
    then uses this number to crop trailing noise bytes.

    Expected framing (default):
        - Header
          - Control         (2 bytes)
          - FEC of control  (1 byte)
          - Callsign        (6 bytes)
          - CRC of Callsign (2 bytes)
        - 1..32 data blocks (num_blocks * 30 bytes)

    ## Variants
    - BEESAT-1: different header (no callsign, no callsign crc)
    - BEESAT-9: Number of datablocks is hard-coded to 32
    - default: no special cases.


    ## Output
    The output is PDUs with one decoded Mobitex block per PDU. The header is
    stripped from the PDU content, but provided in the metadata attached to
    the first Mobitex data block.

    Each block has the following metadata:
        - block_id
    The first block (`block_id`=0) additionally has the following metadata:
        - frame_header - the error-corrected frame header
        - control_errors_corrected
        - callsign_bit_errors
        - num_blocks

    ## Callsign
    If callsign is provided, the received callsign+crc is checked
    against this reference. The callsign check passes if the number of
    detected bit errors does not exceed `callsign_threshold`.

    If no callsign is provided, we try to error-correct callsign+crc
    by flipping bits until CRC matches or a maximum number of bit-flips
    specified by `callsign_threshold` is exceeded.

    # References
    [1]: https://destevez.net/2016/09/some-notes-on-beesat-and-mobitex-nx/
    """
    def __init__(
        self,
        variant: str,
        callsign: Optional[str] = None,
        drop_invalid_control: bool = False,
        callsign_threshold: int = 2,
        verbose=False,
    ):
        gr.basic_block.__init__(self,
                                name="mobitex_to_datablocks",
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
                'control': slice(0, 2),
                'control_fec': slice(2, 3),
            }
        else:
            self.parse_callsign = True
            self.header_length = 2 + 1 + 6 + 2
            self.bytemap = {
                'control': slice(0, 2),
                'control_fec': slice(2, 3),
                'callsign': slice(3, 9),
                'callsign_crc': slice(9, 11),
            }

        if variant == 'BEESAT-9':
            self.num_blocks_hardcoded = True
            self.num_blocks = 32
        else:
            self.num_blocks_hardcoded = False

        # (18 message bytes + 2 CRC bytes), encoded with r=12/8 FEC
        self.block_size = 30

        self.message_port_register_in(pmt.intern("in"))
        self.set_msg_handler(pmt.intern("in"), self.handle_msg)
        self.message_port_register_out(pmt.intern("out"))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return

        packet = pmt.u8vector_elements(msg)

        control = packet[self.bytemap['control']]
        control_fec = packet[self.bytemap['control_fec']]

        result = decode_control(control[0], control[1], control_fec[0])
        if result is None:
            # Decoding of control bytes failed, bit errors uncorrectable
            control_fec_valid = False
            control_bit_errors = -1
        else:
            # Decoding of control bytes succeded.
            control_fec_valid = True
            corrected, control_bit_errors = result

            (control[0], control[1], control_fec[0]) = corrected

            # Apply error-correction
            packet[self.bytemap['control']] = control
            packet[self.bytemap['control_fec']] = control_fec

        if self.drop_invalid_control and not control_fec_valid:
            return

        if self.num_blocks_hardcoded:
            num_blocks = self.num_blocks
        else:
            num_blocks = (control[0] & 0b0001_1111) + 1

        if self.parse_callsign:
            if self.callsign_ref:
                callsign = self.callsign_ref
                callsign_crc, callsign_bit_errors = compare_expected_callsign(
                    bytes(packet[self.bytemap['callsign']]),
                    bytes(packet[self.bytemap['callsign_crc']]),
                    self.callsign_ref,
                )

                if callsign_bit_errors > self.callsign_threshold:
                    # Number of detected bit errors exceeds threshold
                    return
            else:
                result = decode_unknown_callsign(
                    bytes(packet[self.bytemap['callsign']]),
                    bytes(packet[self.bytemap['callsign_crc']]),
                    self.callsign_threshold,
                )

                if result is None:
                    # No valid callsign+crc found within maximum number of
                    # tested bit flips (self.callsign_threshold)
                    return

                callsign, callsign_crc, callsign_bit_errors = result

            try:
                callsign.decode("ascii")
            except UnicodeDecodeError:
                # Drop frame with non-ASCII callsign
                # (empirically this is always a false-positive syncword match)
                return

            # Apply error-correction
            packet[self.bytemap['callsign']] = callsign
            packet[self.bytemap['callsign_crc']] = callsign_crc
        else:
            # Skip callsign decoding
            pass

        frame_header = packet[: self.header_length]

        blocks_start = self.header_length
        blocks_end = self.header_length + self.block_size * num_blocks
        data_blocks = packet[blocks_start:blocks_end]

        blocks = (data_blocks[a:a + self.block_size]
                  for a in range(0, len(data_blocks), self.block_size))

        for block_idx, block in enumerate(blocks):
            if block_idx == 0:
                meta = pmt.make_dict()
                meta = pmt.dict_add(
                    meta,
                    pmt.intern("control_errors_corrected"),
                    pmt.from_long(control_bit_errors),
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
