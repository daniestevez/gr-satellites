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

#include "ra_config.h"
#include <assert.h>

/* masks selected from http://users.ece.cmu.edu/~koopman/lfsr/index.html */
static uint16_t ra_lfsr_masks_table[9][4] = {
    {0x12, 0x17, 0x1B, 0x1E},         // highbit 4, data_length <= 31
    {0x21, 0x2D, 0x30, 0x39},         // highbit 5, data_length <= 63
    {0x41, 0x53, 0x69, 0x7B},         // highbit 6, data_length <= 127
    {0x8E, 0xAF, 0xC3, 0xE7},         // highbit 7, data_length <= 255
    {0x108, 0x13B, 0x168, 0x1DC},     // highbit 8, data_length <= 511
    {0x204, 0x2E3, 0x369, 0x3AA},     // highbit 9, data_length <= 1023
    {0x415, 0x4BF, 0x553, 0x62B},     // highbit 10, data_length <= 2047
    {0x83E, 0x939, 0xAF5, 0xD70},     // highbit 11, data_length <= 4095
    {0x1013, 0x109D, 0x117D, 0x1271}, // highbit 12, data_length <= 8191
};

ra_index_t ra_data_length = 0;
ra_index_t ra_code_length = 0;
ra_index_t ra_chck_length = 0;
uint16_t ra_lfsr_masks[4];
uint8_t ra_lfsr_highbit;

void ra_length_init(ra_index_t data_length) {
  assert(4 <= data_length && data_length <= RA_MAX_DATA_LENGTH);

  ra_data_length = data_length;
  ra_chck_length = (data_length + RA_PUNCTURE_RATE - 1) / RA_PUNCTURE_RATE;
  ra_code_length = data_length + ra_chck_length * 3;
  assert(ra_code_length <= RA_MAX_CODE_LENGTH);

  ra_lfsr_highbit = 4;
  while (data_length >= 32) {
    data_length /= 2;
    ra_lfsr_highbit += 1;
  }
  assert(4 <= ra_lfsr_highbit && ra_lfsr_highbit <= 12);

  ra_lfsr_masks[0] = ra_lfsr_masks_table[ra_lfsr_highbit - 4][0];
  ra_lfsr_masks[1] = ra_lfsr_masks_table[ra_lfsr_highbit - 4][1];
  ra_lfsr_masks[2] = ra_lfsr_masks_table[ra_lfsr_highbit - 4][2];
  ra_lfsr_masks[3] = ra_lfsr_masks_table[ra_lfsr_highbit - 4][3];

}
