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

#ifndef RA_CONFIG_H
#define RA_CONFIG_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef uint16_t ra_word_t;  /* use uint16_t for SSE4.1 soft decoder */
typedef uint16_t ra_index_t; /* use uint16_t for RA_PACKET_LENGTH >= 256 */

enum {
    /* number of words, must be at least 4 */
    RA_MAX_DATA_LENGTH = 2048,

    /* 1 for rate 1/4, 2 for 2/5, 3 for 1/2, 5 for 5/8 */
    RA_PUNCTURE_RATE = 3,

    /* use the test program to verify it */
    RA_MAX_CODE_LENGTH = RA_MAX_DATA_LENGTH * 2 + 3,
};

enum { RA_BITCOUNT = 8 * sizeof(ra_word_t), RA_BITSHIFT = RA_BITCOUNT - 1 };

struct ra_context {
    ra_index_t ra_data_length;
    ra_index_t ra_code_length;
    ra_index_t ra_chck_length;
    uint16_t ra_lfsr_masks[4];
    uint8_t ra_lfsr_highbit;

    // for ra_lfsr
    ra_index_t ra_lfsr_mask;
    ra_index_t ra_lfsr_state;
    ra_index_t ra_lfsr_offset;

    // for ra_decoder_gen
    float ra_dataword_gen[RA_MAX_DATA_LENGTH * RA_BITCOUNT];
    float ra_codeword_gen[RA_MAX_CODE_LENGTH * RA_BITCOUNT];
    float ra_forward_gen[RA_MAX_DATA_LENGTH * RA_BITCOUNT];

    // for ra_encoder
    const ra_word_t* ra_packet;
    ra_word_t ra_nextword;
    uint8_t ra_passno;
};

/* data length in words */
void ra_length_init(struct ra_context* ctx, ra_index_t data_length);

#ifdef __cplusplus
}
#endif

#endif // RA_CONFIG_H
