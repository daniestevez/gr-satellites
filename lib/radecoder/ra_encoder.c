/* -*- c++ -*- */
/*
 * Copyright (C) Miklos Maroti 2015
 * Obtained from https://gitlab.com/phorvath/smogcli2
 * Copyright 2020 Daniel Estevez <daniel@destevez.net> (adaptation to gr-satellites)
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#include "ra_encoder.h"
#include "ra_lfsr.h"

/* --- REPEAT ACCUMULATE ENCODER: rate 1/4, punctured, twisted parallel --- */

void ra_encoder_init(struct ra_context* ctx, const ra_word_t* packet)
{
    ctx->ra_packet = packet;
    ctx->ra_nextword = 0;
    ctx->ra_passno = 0;
    ra_lfsr_init(ctx, 0);
}

ra_word_t ra_encoder_next(struct ra_context* ctx)
{
    ra_index_t pos;
    ra_word_t word;
    uint8_t count;

    word = ctx->ra_nextword;

    count = ctx->ra_passno == 0 ? 1 : RA_PUNCTURE_RATE;
    do {
        word = (word >> 1) | (word << RA_BITSHIFT);
        pos = ra_lfsr_next(ctx);
        word ^= ctx->ra_packet[pos];
    } while (pos != ctx->ra_passno && --count != 0);

    if (count != 0) {
        ctx->ra_nextword = 0;
        ctx->ra_passno = (ctx->ra_passno + 1) % 4;
        ra_lfsr_init(ctx, ctx->ra_passno);
    } else
        ctx->ra_nextword = word;

    return word;
}

void ra_encoder(struct ra_context* ctx, const ra_word_t* packet, ra_word_t* output)
{
    ra_encoder_init(ctx, packet);
    for (ra_index_t i = 0; i < ctx->ra_code_length; i++)
        *(output++) = ra_encoder_next(ctx);
}
