/*
 * Copyright 2015-2019 Miklos Maroti.
 * Copyright 2019 Daniel Estevez <daniel@destevez.net> (reentrant version)
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */


#include "ra_lfsr.h"
#include <assert.h>

/* last element returned will be seqno */
void ra_lfsr_init(struct ra_context *ctx, uint8_t seqno) {
  /* make sure that ra_length_init is called */
  assert(ctx->ra_data_length > 0);

  ctx->ra_lfsr_mask = ctx->ra_lfsr_masks[seqno];
  ctx->ra_lfsr_offset = ctx->ra_data_length >> (1 + seqno);
  ctx->ra_lfsr_state = 1 + seqno + ctx->ra_lfsr_offset;
}

ra_index_t ra_lfsr_next(struct ra_context *ctx) {
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

ra_index_t ra_lfsr_prev(struct ra_context *ctx) {
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
