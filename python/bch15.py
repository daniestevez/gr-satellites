#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# BCH(15,k,d) implementation following https://en.wikipedia.org/wiki/BCH_code

import numpy as np

# Arithmetic in GF(16)

# exp_table[k] = a^k
exp_table = [8, 4, 2, 1, 12, 6, 3, 13, 10, 5, 14, 7, 15, 11, 9]
# j+1 = a^log_table[j]
log_table = [3, 2, 6, 1, 9, 5, 11, 0, 14, 8, 13, 4, 7, 10, 12]


def gf_mult(x, y):
    if x == 0 or y == 0:
        return 0
    return exp_table[(log_table[x-1] + log_table[y-1]) % len(exp_table)]


def gf_inv(x):
    if x == 0:
        raise(ValueError)
    return exp_table[-log_table[x-1] % len(exp_table)]


def compute_syndrome(p, j):
    # Syndrome calculation by polynomial evaluation
    s = 0
    n = 15
    for k in range(n - 1, -1, -1):
        if p & 1:
            s ^= exp_table[(k * j) % len(exp_table)]
        p >>= 1
    return s


def compute_error_locations(s):
    # Peterson-Gorenstein-Zierler algorithm
    L = [1, 0, 0, 0]  # coefficients of error locator polynomial
    if len(s) == 2:
        # This will raise ValueError if s[0] == 0, indicating decoding failure
        L[1] = gf_mult(s[1], gf_inv(s[0]))
    elif len(s) == 4:
        det_S = gf_mult(s[0], s[2]) ^ gf_mult(s[1], s[1])
        if det_S == 0:
            # Matrix is non-invertible. Throw away 2 syndromes.
            return compute_error_locations(s[:-2])
        inv_det_S = gf_inv(det_S)
        L[2] = gf_mult(s[2], s[2]) ^ gf_mult(s[3], s[1])
        L[2] = gf_mult(L[2], inv_det_S)
        L[1] = gf_mult(s[0], s[3]) ^ gf_mult(s[2], s[1])
        L[1] = gf_mult(L[1], inv_det_S)
    elif len(s) == 6:
        det_S = (
            gf_mult(gf_mult(s[0], s[2]), s[4])
            ^ gf_mult(gf_mult(s[2], s[2]), s[2])
            ^ gf_mult(gf_mult(s[1], s[1]), s[4])
            ^ gf_mult(gf_mult(s[3], s[3]), s[0]))
        if det_S == 0:
            # Matrix is non-invertible. Throw away 2 syndromes.
            return compute_error_locations(s[:-2])
        inv_det_S = gf_inv(det_S)
        L[3] = (
            gf_mult(gf_mult(s[3], s[2]), s[4])
            ^ gf_mult(gf_mult(s[1], s[3]), s[5])
            ^ gf_mult(gf_mult(s[4], s[3]), s[2])
            ^ gf_mult(gf_mult(s[2], s[2]), s[5])
            ^ gf_mult(gf_mult(s[1], s[4]), s[4])
            ^ gf_mult(gf_mult(s[3], s[3]), s[3]))
        L[3] = gf_mult(L[3], inv_det_S)
        L[2] = (
            gf_mult(gf_mult(s[0], s[4]), s[4])
            ^ gf_mult(gf_mult(s[1], s[2]), s[5])
            ^ gf_mult(gf_mult(s[3], s[3]), s[2])
            ^ gf_mult(gf_mult(s[2], s[2]), s[4])
            ^ gf_mult(gf_mult(s[1], s[3]), s[4])
            ^ gf_mult(gf_mult(s[0], s[3]), s[5]))
        L[2] = gf_mult(L[2], inv_det_S)
        L[1] = (
            gf_mult(gf_mult(s[0], s[2]), s[5])
            ^ gf_mult(gf_mult(s[1], s[3]), s[3])
            ^ gf_mult(gf_mult(s[4], s[1]), s[2])
            ^ gf_mult(gf_mult(s[2], s[2]), s[3])
            ^ gf_mult(gf_mult(s[1], s[1]), s[5])
            ^ gf_mult(gf_mult(s[0], s[3]), s[4]))
        L[1] = gf_mult(L[1], inv_det_S)
    # Brute-force search roots of error locator polynomial
    return [j for j in range(15) if
            exp_table[0]
            ^ gf_mult(L[1], exp_table[-j % len(exp_table)])
            ^ gf_mult(L[2], exp_table[-2*j % len(exp_table)])
            ^ gf_mult(L[3], exp_table[-3*j % len(exp_table)])
            == 0]


def decode_bch15(bits, d=7):
    """BCH(15,k,d) decode function

The following values of (n,k,d) are supported:
(15,11,3), (15,7,5), (15,5,7)

Expects an np.array() as bits and modifies it in place
returns True if decode is successful
"""
    b = np.packbits(bits)
    p = (b[0] << 7) | (b[1] >> 1)
    syndromes = [compute_syndrome(p, j) for j in range(d - 1)]
    if not any(syndromes):
        # If all syndromes are zero, there are no errors
        return True
    try:
        errors = compute_error_locations(syndromes)
    except ValueError:
        return False
    for e in errors:
        bits[e] ^= 1
    return True
