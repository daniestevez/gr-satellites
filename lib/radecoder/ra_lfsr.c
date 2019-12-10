/*
 * Copyright 2015-2019 Miklos Maroti.
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

static ra_index_t ra_lfsr_mask;
static ra_index_t ra_lfsr_state;
static ra_index_t ra_lfsr_offset;

/* last element returned will be seqno */
void ra_lfsr_init(uint8_t seqno) {
  /* make sure that ra_length_init is called */
  assert(ra_data_length > 0);

  ra_lfsr_mask = ra_lfsr_masks[seqno];
  ra_lfsr_offset = ra_data_length >> (1 + seqno);
  ra_lfsr_state = 1 + seqno + ra_lfsr_offset;
}

ra_index_t ra_lfsr_next(void) {
  ra_index_t b;

  /* this loop runs at most twice on average */
  do {
    b = ra_lfsr_state & 0x1;
    ra_lfsr_state >>= 1;
    ra_lfsr_state ^= (-b) & ra_lfsr_mask;
  } while (ra_lfsr_state > ra_data_length);

  b = ra_lfsr_state - 1;
  if (b < ra_lfsr_offset)
    b += ra_data_length;
  b -= ra_lfsr_offset;
  return b;
}

ra_index_t ra_lfsr_prev(void) {
  ra_index_t b;

  /* this loop runs at most twice on average */
  do {
    b = ra_lfsr_state >> ra_lfsr_highbit;
    ra_lfsr_state <<= 1;
    ra_lfsr_state ^= (-b) & (0x01 | ra_lfsr_mask << 1);
  } while (ra_lfsr_state > ra_data_length);

  b = ra_lfsr_state - 1;
  if (b < ra_lfsr_offset)
    b += ra_data_length;
  b -= ra_lfsr_offset;
  return b;
}
