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


#ifndef RA_DECODER_GEN_H
#define RA_DECODER_GEN_H

#include "ra_config.h"

#ifdef __cplusplus
extern "C" {
#endif

void ra_decoder_gen(float *softbits, ra_word_t *packet, int passes);

#ifdef __cplusplus
}
#endif

#endif // RA_DECODER_GEN_H
