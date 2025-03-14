#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
Implementation of the Mobitex FEC

This module implements the FEC algorithm used in the Mobitex protocol
for error detection and correction.

It is a (12,8,3) linear code, thus it can encode 8-bit data with 4-bit
FEC codes and detect/correct single-bit errors in the combined 12-bit words.

- Reliable two-bit error correction is not possible with this FEC scheme.
- Many collisions occur where a two-bit error produces the same syndrome as
  a single-bit error.

References:
[1]: ttps://git.tu-berlin.de/rft/com/mobitub-2/-/blob/master/gr-tnc_nx/
[2]: MIT OpenCourseWare 6.02
     Introduction to EECS II: Digital Communication Systems
     Chapter 5: Coping with Bit Errors using Error Correction Codes
     https://ocw.mit.edu/courses/
[3]: https://destevez.net/2016/09/some-notes-on-beesat-and-mobitex-nx/
"""
import sys

from enum import IntEnum

# Matrix H, in 8 and 12 column variant
FEC_MATRIX_8b = [
    0b11101100,
    0b11010011,
    0b10111010,
    0b01110101,
]
FEC_MATRIX_12b = [
    0b11101100_1000,
    0b11010011_0100,
    0b10111010_0010,
    0b01110101_0001,
]


class Status(IntEnum):
    NO_ERROR = 0
    ERROR_CORRECTED = 1
    ERROR_UNCORRECTABLE = 2


if sys.version_info >= (3, 10):
    def calculate_even_parity(value: int) -> int:
        return value.bit_count() & 1
else:
    def calculate_even_parity(value: int) -> int:
        """Calculate even parity of a value, using XOR folding.

        value must be 16-bit or smaller.

        Returns:
            Integer (0 or 1) representing (even or odd) parity
        """
        value ^= (value >> 16)
        value ^= (value >> 8)
        value ^= (value >> 4)
        value ^= (value >> 2)
        value ^= (value >> 1)

        return value & 1


def init_syndrome_table() -> dict:
    """Initialize the syndrome lookup table.

    Returns:
        Dict mapping syndromes to error positions
    """
    table = {}

    # Process each possible single-bit error position
    for pos in range(12):  # 12 bits total (8 data + 4 FEC)
        # Create word with error at position pos
        word = 1 << pos

        # Calculate syndrome for this error
        syndrome = 0
        for i, mask in enumerate(FEC_MATRIX_12b):
            masked = word & mask
            parity = calculate_even_parity(masked)
            syndrome |= (parity << (3 - i))

        table[syndrome] = pos
    return table


SYNDROME_TABLE = init_syndrome_table()


def encode(message: int) -> int:
    """
    Takes 8-bit byte, returns 12-bit codeword.
    """
    fec = 0
    # Generate each FEC bit and place in correct position
    for i, mask in enumerate(FEC_MATRIX_8b):
        masked = message & mask
        parity = calculate_even_parity(masked)

        # Place parity bit in correct position (3-0)
        fec |= (parity << (3 - i))

    # Combine data byte and FEC into 12-bit codeword
    codeword = (message << 4) | fec

    return codeword


def decode(codeword: int):
    """
    Takes 12-bit codeword, returns tuple of (message, corrected_fec, status).

    output:
        corrected_message (int): 1 control byte, error corrected
        corrected_fec (int)    : 4 parity bits, error corrected
        status (Status)        : (0 - NO ERROR,
                                  1 - ERROR CORRECTED,
                                  2 - ERROR UNCORRECTABLE)
    """
    if not 0 <= codeword <= 0xFFF:
        raise ValueError("Input must be a 12-bit value (0-4095)")

    syndrome = 0
    for i, row in enumerate(FEC_MATRIX_12b):
        masked = codeword & row
        parity = calculate_even_parity(masked)

        # Build syndrome from right to left (like FEC bits)
        syndrome |= (parity << (3 - i))

    if syndrome == 0:
        message = codeword >> 4
        fec = codeword & 0x0F
        return message, fec, Status.NO_ERROR

    # Look up error position in syndrome table
    try:
        error_position = SYNDROME_TABLE[syndrome]
    except KeyError:
        message = codeword >> 4
        fec = codeword & 0x0F
        return message, fec, Status.ERROR_UNCORRECTABLE

    # Correct the error by flipping the bit
    corrected = codeword ^ (1 << error_position)

    message = corrected >> 4
    fec = corrected & 0x0F
    return message, fec, Status.ERROR_CORRECTED


def split(word: int) -> tuple[int, int]:
    """Split 12-bit codeword into data byte and FEC."""
    return (word >> 4), (word & 0xF)


def pack_2b(byte0: int, byte1: int) -> bytes:
    """Pack two 12-bit codewords into three bytes."""
    encoded_byte1 = byte0 >> 4
    encoded_byte2 = ((byte0 & 0x0F) << 4) | (byte1 >> 8)
    encoded_byte3 = byte1 & 0xFF
    return bytes([encoded_byte1, encoded_byte2, encoded_byte3])


def unpack_2b(code: bytes) -> tuple[int, int]:
    """From three bytes unpack two 12-bit codewords."""
    codeword0 = (code[0] << 4) | (code[1] >> 4)
    codeword1 = ((code[1] & 0x0F) << 8) | code[2]
    return codeword0, codeword1
