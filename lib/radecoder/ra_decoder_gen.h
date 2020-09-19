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

#ifndef RA_DECODER_GEN_H
#define RA_DECODER_GEN_H

#include "ra_config.h"

#ifdef __cplusplus
extern "C" {
#endif

void ra_decoder_gen(struct ra_context* ctx,
                    float* softbits,
                    ra_word_t* packet,
                    int passes);

#ifdef __cplusplus
}
#endif

#endif // RA_DECODER_GEN_H
