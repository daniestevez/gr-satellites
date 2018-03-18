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

# BCH(15,k,d) implementation following https://en.wikipedia.org/wiki/BCH_code

# arithmetic in GF(16)

import numpy as np

exp_table = [8, 4, 2, 1, 12, 6, 3, 13, 10, 5, 14, 7, 15, 11, 9] # exp_table[k] = a^k
log_table = [3, 2, 6, 1, 9, 5, 11, 0, 14, 8, 13, 4, 7, 10, 12] # j+1 = a^log_table[j]

def gf_mult(x,y):
    if x == 0 or y == 0:
        return 0
    return exp_table[(log_table[x-1] + log_table[y-1]) % len(exp_table)]

def gf_inv(x):
    if x == 0:
        raise(ValueError)
    return exp_table[-log_table[x-1] % len(exp_table)]

# syndrome calculation by polynomial evaluation

def compute_syndrome(p,j):
    s = 0
    n = 15
    for k in range(n-1,-1,-1):
        if p & 1:
            s ^= exp_table[(k * j) % len(exp_table)]
        p >>= 1
    return s

# Peterson-Gorenstein-Zierler algorithm

def compute_error_locations(s):
    l = [1,0,0,0] # coefficients of error locator polynomial
    if len(s) == 2:
        l[1] = gf_mult(s[1], gf_inv(s[0])) # will raise ValueError if s[0] == 0, indicating decoding failure
    elif len(s) == 4:
        det_S = gf_mult(s[0], s[2]) ^ gf_mult(s[1], s[1])
        if det_S == 0:
            return compute_error_locations(s[:-2]) # matrix is non-invertible, throw away 2 syndromes
        inv_det_S = gf_inv(det_S)
        l[2] = gf_mult(s[2],s[2]) ^ gf_mult(s[3], s[1])
        l[2] = gf_mult(l[2], inv_det_S)
        l[1] = gf_mult(s[0], s[3]) ^ gf_mult(s[2], s[1])
        l[1] = gf_mult(l[1], inv_det_S)
    elif len(s) == 6:
        det_S = gf_mult(gf_mult(s[0], s[2]), s[4]) ^ gf_mult(gf_mult(s[2], s[2]), s[2]) \
        ^ gf_mult(gf_mult(s[1], s[1]), s[4]) ^ gf_mult(gf_mult(s[3], s[3]), s[0])
        if det_S == 0:
            return compute_error_locations(s[:-2]) # matrix is non-invertible, throw away 2 syndromes
        inv_det_S = gf_inv(det_S)
        l[3] = gf_mult(gf_mult(s[3], s[2]), s[4]) ^ gf_mult(gf_mult(s[1], s[3]), s[5]) \
            ^ gf_mult(gf_mult(s[4], s[3]), s[2]) \
            ^ gf_mult(gf_mult(s[2], s[2]), s[5]) ^ gf_mult(gf_mult(s[1], s[4]), s[4]) \
            ^ gf_mult(gf_mult(s[3], s[3]), s[3])
        l[3] = gf_mult(l[3], inv_det_S)
        l[2] = gf_mult(gf_mult(s[0], s[4]), s[4]) ^ gf_mult(gf_mult(s[1], s[2]), s[5]) \
            ^ gf_mult(gf_mult(s[3], s[3]), s[2]) \
            ^ gf_mult(gf_mult(s[2], s[2]), s[4]) ^ gf_mult(gf_mult(s[1], s[3]), s[4]) \
            ^ gf_mult(gf_mult(s[0], s[3]), s[5])
        l[2] = gf_mult(l[2], inv_det_S)
        l[1] = gf_mult(gf_mult(s[0], s[2]), s[5]) ^ gf_mult(gf_mult(s[1], s[3]), s[3]) \
            ^ gf_mult(gf_mult(s[4], s[1]), s[2]) \
            ^ gf_mult(gf_mult(s[2], s[2]), s[3]) ^ gf_mult(gf_mult(s[1], s[1]), s[5]) \
            ^ gf_mult(gf_mult(s[0], s[3]), s[4])
        l[1] = gf_mult(l[1], inv_det_S)
    # brute-force search roots of error locator polynomial
    return [j for j in range(15) if \
     exp_table[0] ^ gf_mult(l[1], exp_table[-j % len(exp_table)]) \
     ^ gf_mult(l[2], exp_table[-2*j % len(exp_table)]) ^ gf_mult(l[3], exp_table[-3*j % len(exp_table)]) == 0]

# Decode function. The following values of (n,k,d) are supported:
# (15,11,3), (15,7,5), (15,5,7)
# Expects an np.array() as bits and modifies it in place
# returns True if decode is successful

def decode_bch15(bits, d = 7):
    b = np.packbits(bits)
    p = (b[0] << 7) | (b[1] >> 1)
    syndromes = [compute_syndrome(p, j) for j in range(d-1)]
    if not any(syndromes):
        # if all syndromes are zero, there are no errors
        return True
    try:
        errors = compute_error_locations(syndromes)
    except ValueError:
        return False
    for e in errors:
        bits[e] ^= 1
    return True
