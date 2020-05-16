/* -*- c -*- */
/*
 * Copyright 2015-2019 Miklos Maroti
 * Copyright 2019 Daniel Estevez <daniel@destevez.net> (reentrant version)
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#include "ra_decoder_gen.h"
#include "ra_lfsr.h"
#include <assert.h>
#include <float.h>
#include <math.h>
#include <stdbool.h>

/* --- REPEAT ACCUMULATE GENERIC DECODER --- */

void ra_prepare_gen(struct ra_context *ctx, float *softbits) {
  int index;

  for (index = 0; index < ctx->ra_data_length * RA_BITCOUNT; index++)
    ctx->ra_dataword_gen[index] = 0.0f;

  for (index = 0; index < ctx->ra_code_length * RA_BITCOUNT; index++)
    ctx->ra_codeword_gen[index] = softbits[index];
}

static inline float ra_llr_min(float a, float b) {
  float c;

  c = a * b;
  a = fabsf(a);
  b = fabsf(b);

  a = a < b ? a : b;
  return copysignf(a, c);
}

void ra_improve_gen(struct ra_context *ctx, float *codeword, int puncture, bool half) {
  int index, bit, pos;
  float accu[RA_BITCOUNT];
  float data, left;

  assert(ctx->ra_data_length > 0); /* to avoid pos uninitialized warning */

  for (bit = 0; bit < RA_BITCOUNT; bit++)
    accu[bit] = FLT_MAX;

  for (index = 0; index < ctx->ra_data_length; index++) {
    pos = ra_lfsr_next(ctx);

    for (bit = 0; bit < RA_BITCOUNT; bit++) {
      data = ctx->ra_dataword_gen[pos * RA_BITCOUNT + bit];
      ctx->ra_forward_gen[index * RA_BITCOUNT + bit] = accu[bit];
      accu[bit] = ra_llr_min(accu[bit], data);
    }

    if ((index + 1) % puncture == 0) {
      for (bit = 0; bit < RA_BITCOUNT; bit++)
        accu[bit] += *(codeword++);
    }

    data = accu[0];
    for (bit = 0; bit < RA_BITCOUNT - 1; bit++)
      accu[bit] = accu[bit + 1];
    accu[RA_BITCOUNT - 1] = data;
  }

  if (ctx->ra_data_length % puncture != 0) {
    for (bit = 0; bit < RA_BITCOUNT; bit++) {
      data = codeword[(bit + 1) % RA_BITCOUNT];
      accu[bit] = accu[bit] + data + data;
    }
  }

  for (index = ctx->ra_data_length - 1; index >= 0; index--) {
    data = accu[RA_BITCOUNT - 1];
    for (bit = RA_BITCOUNT - 1; bit >= 1; bit--)
      accu[bit] = accu[bit - 1];
    accu[0] = data;

    if ((index + 1) % puncture == 0) {
      for (bit = RA_BITCOUNT - 1; bit >= 0; bit--)
        accu[bit] += *(--codeword);
    }

    for (bit = 0; bit < RA_BITCOUNT; bit++) {
      left = ctx->ra_forward_gen[index * RA_BITCOUNT + bit];
      left = ra_llr_min(left, accu[bit]);

      data = ctx->ra_dataword_gen[pos * RA_BITCOUNT + bit];
      accu[bit] = ra_llr_min(accu[bit], data);

      if (half)
        data *= 0.5f;

      left += data;
      ctx->ra_dataword_gen[pos * RA_BITCOUNT + bit] = left;
    }

    pos = ra_lfsr_prev(ctx);
  }
}

void ra_decide_gen(struct ra_context *ctx, ra_word_t *packet) {
  int index, bit;
  ra_word_t word;
  float data;

  for (index = 0; index < ctx->ra_data_length; index++) {
    word = 0;

    for (bit = 0; bit < RA_BITCOUNT; bit++) {
      data = ctx->ra_dataword_gen[index * RA_BITCOUNT + bit];
      word |= (data < 0.0f) << bit;
    }

    packet[index] = word;
  }
}

void ra_decoder_gen(struct ra_context *ctx, float *softbits, ra_word_t *packet, int passes) {
  int count, seqno;
  float *codeword;

  ra_prepare_gen(ctx, softbits);

  for (count = 0; count < passes; count++) {
    codeword = ctx->ra_codeword_gen;

    for (seqno = 0; seqno < 4; seqno++) {
      ra_lfsr_init(ctx, seqno);
      ra_improve_gen(ctx, codeword, seqno == 0 ? 1 : RA_PUNCTURE_RATE, count > 0);
      codeword += (seqno == 0 ? ctx->ra_data_length : ctx->ra_chck_length) * RA_BITCOUNT;
    }

    assert(ctx->ra_codeword_gen + ctx->ra_code_length * RA_BITCOUNT == codeword);
  }

  ra_decide_gen(ctx, packet);
}
