/* -*- c -*- */
/*
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/*
 This algorithm is based on 
 R.H. Morelos-Zaragoza, The Art of Error Correcting Coding, Wiley, 2002; Section 2.2.3
*/

#ifndef _GOLAY24_H
#define _GOLAY24_H

#include <stdint.h>

int decode_golay24(uint32_t *data);
int encode_golay24(uint32_t *data);

#endif
