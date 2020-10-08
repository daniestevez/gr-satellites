/* -*- c -*- */
/*
 * Copyright 2015-2019 Miklos Maroti.
 * Copyright 2019 Daniel Estevez <daniel@destevez.net> (reentrant version)
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#include "ra_config.h"
#include <assert.h>

/* masks selected from http://users.ece.cmu.edu/~koopman/lfsr/index.html */
static const uint16_t ra_lfsr_masks_table[9][4] = {
    { 0x12, 0x17, 0x1B, 0x1E },         // highbit 4, data_length <= 31
    { 0x21, 0x2D, 0x30, 0x39 },         // highbit 5, data_length <= 63
    { 0x41, 0x53, 0x69, 0x7B },         // highbit 6, data_length <= 127
    { 0x8E, 0xAF, 0xC3, 0xE7 },         // highbit 7, data_length <= 255
    { 0x108, 0x13B, 0x168, 0x1DC },     // highbit 8, data_length <= 511
    { 0x204, 0x2E3, 0x369, 0x3AA },     // highbit 9, data_length <= 1023
    { 0x415, 0x4BF, 0x553, 0x62B },     // highbit 10, data_length <= 2047
    { 0x83E, 0x939, 0xAF5, 0xD70 },     // highbit 11, data_length <= 4095
    { 0x1013, 0x109D, 0x117D, 0x1271 }, // highbit 12, data_length <= 8191
};

void ra_length_init(struct ra_context* ctx, ra_index_t data_length)
{
    assert(4 <= data_length && data_length <= RA_MAX_DATA_LENGTH);

    ctx->ra_data_length = data_length;
    ctx->ra_chck_length = (data_length + RA_PUNCTURE_RATE - 1) / RA_PUNCTURE_RATE;
    ctx->ra_code_length = data_length + ctx->ra_chck_length * 3;
    assert(ctx->ra_code_length <= RA_MAX_CODE_LENGTH);

    ctx->ra_lfsr_highbit = 4;
    while (data_length >= 32) {
        data_length /= 2;
        ctx->ra_lfsr_highbit += 1;
    }
    assert(4 <= ctx->ra_lfsr_highbit && ctx->ra_lfsr_highbit <= 12);

    ctx->ra_lfsr_masks[0] = ra_lfsr_masks_table[ctx->ra_lfsr_highbit - 4][0];
    ctx->ra_lfsr_masks[1] = ra_lfsr_masks_table[ctx->ra_lfsr_highbit - 4][1];
    ctx->ra_lfsr_masks[2] = ra_lfsr_masks_table[ctx->ra_lfsr_highbit - 4][2];
    ctx->ra_lfsr_masks[3] = ra_lfsr_masks_table[ctx->ra_lfsr_highbit - 4][3];
}
