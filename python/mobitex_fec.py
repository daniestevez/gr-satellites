#!/usr/bin/env python3
# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
from enum import IntEnum

# Matrix H, in 8 and 12 column variant
FEC_MATRIX_8b = [
    0xEC,  # 11101100
    0xD3,  # 11010011
    0xBA,  # 10111010
    0x75   # 01110101
]
FEC_MATRIX_12b = [
    0xEC8,  # 11101100 1000
    0xD34,  # 11010011 0100
    0xBA2,  # 10111010 0010
    0x751   # 01110101 0001
]


class Status(IntEnum):
    NO_ERROR = 0
    ERROR_CORRECTED = 1
    ERROR_UNCORRECTABLE = 2


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


def _init_syndrome_table() -> dict:
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


# SYNDROME_TABLE = {
#     1: 0, 2: 1, 4: 2, 8: 3, 5: 4, 6: 5,
#     9: 6, 10: 7, 7: 8, 11: 9, 13: 10, 14: 11}
SYNDROME_TABLE = _init_syndrome_table()


def encode(message: int) -> tuple[int, int]:
    """
    Takes 8-bit byte, returns tuple of (12-bit codeword, 4-bit fec)
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

    return codeword, fec


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
    error_position = SYNDROME_TABLE.get(syndrome, -1)

    if error_position == -1:
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


def test_roundtrip():
    message = 0x2C
    print('Example with zero bit errors:')
    print(f'message:  0x{message:02X}')
    codeword, fec = encode(message)
    print(f'codeword: 0x{codeword:03X}')
    print(f'fec:      0x  {fec:01X}')
    assert fec == 0x08

    corrected, _, status = decode(codeword)
    print(status)
    assert status == Status.NO_ERROR
    assert corrected == message

    print('\nExample with single-bit error:')
    codeword = codeword | 0b0010_0000
    corrected, _, status = decode(codeword)
    print(f'message:   0x{message:02X}')
    print(f'codeword:  0x{codeword:03X}')
    print(f'corrected: 0x{corrected:02X}')
    print(status)

    print('\nExample with two-bit error:')
    codeword = codeword | 0b0010_0010
    corrected, _, status = decode(codeword)
    print(f'message:   0x{message:02X}')
    print(f'codeword:  0x{codeword:03X}')
    print(f'corrected: 0x{corrected:02X}')
    print(status)

    print('\nExample of encoding 2 bytes:')
    message0 = 0x01
    message1 = 0x02
    codeword0, fec0 = encode(message0)
    codeword1, fec1 = encode(message1)
    code = pack_2b(codeword0, codeword1)

    unpacked_codeword0, unpacked_codeword1 = unpack_2b(code)
    corrected0, _, status0 = decode(unpacked_codeword0)
    corrected1, _, status1 = decode(unpacked_codeword1)

    print(f'message0:   0x{message0:02X}')
    print(f'message1:   0x{message1:02X}')
    print(f'codeword0:  0x{codeword0:03X}')
    print(f'codeword1:  0x{codeword1:03X}')
    print(f'code:    0x{code.hex()}')
    print('---')
    print(f'corrected0: 0x{corrected0:02X}')
    print(f'corrected1: 0x{corrected1:02X}')


def test_edge_cases():
    """Test edge cases and error conditions."""

    # Test all possible 8-bit values
    for i in range(256):
        codeword, fec = encode(i)
        assert 0 <= fec <= 0xF
        decoded, _, status = decode(codeword)
        assert status == status.NO_ERROR
        assert decoded == i

    # For one example message,
    # test all possible single-bit errors.
    message = 0x2C
    codeword, fec = encode(message)

    for bit in range(12):
        corrupted = codeword ^ (1 << bit)
        decoded, _, status = decode(corrupted)
        assert status == Status.ERROR_CORRECTED
        assert decoded == message


if __name__ == '__main__':
    test_roundtrip()
    test_edge_cases()
