/* -*- c -*- */
/*
 * Copyright 2015-2019 Miklos Maroti
 * Copyright 2017 Daniel Estevez <daniel@destevez.net> (reentrant version)
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#include "ra_lfsr.h"
#include <assert.h>

/* last element returned will be seqno */
void ra_lfsr_init(struct ra_context* ctx, uint8_t seqno)
{
    /* make sure that ra_length_init is called */
    assert(ctx->ra_data_length > 0);

    ctx->ra_lfsr_mask = ctx->ra_lfsr_masks[seqno];
    ctx->ra_lfsr_offset = ctx->ra_data_length >> (1 + seqno);
    ctx->ra_lfsr_state = 1 + seqno + ctx->ra_lfsr_offset;
}

ra_index_t ra_lfsr_next(struct ra_context* ctx)
{
    ra_index_t b;

    /* this loop runs at most twice on average */
    do {
        b = ctx->ra_lfsr_state & 0x1;
        ctx->ra_lfsr_state >>= 1;
        ctx->ra_lfsr_state ^= (-b) & ctx->ra_lfsr_mask;
    } while (ctx->ra_lfsr_state > ctx->ra_data_length);

    b = ctx->ra_lfsr_state - 1;
    if (b < ctx->ra_lfsr_offset)
        b += ctx->ra_data_length;
    b -= ctx->ra_lfsr_offset;
    return b;
}

ra_index_t ra_lfsr_prev(struct ra_context* ctx)
{
    ra_index_t b;

    /* this loop runs at most twice on average */
    do {
        b = ctx->ra_lfsr_state >> ctx->ra_lfsr_highbit;
        ctx->ra_lfsr_state <<= 1;
        ctx->ra_lfsr_state ^= (-b) & (0x01 | ctx->ra_lfsr_mask << 1);
    } while (ctx->ra_lfsr_state > ctx->ra_data_length);

    b = ctx->ra_lfsr_state - 1;
    if (b < ctx->ra_lfsr_offset)
        b += ctx->ra_data_length;
    b -= ctx->ra_lfsr_offset;
    return b;
}
