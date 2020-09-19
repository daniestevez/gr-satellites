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

#ifndef __RA_ENCODER_H__
#define __RA_ENCODER_H__

#include "ra_config.h"

#ifdef __cplusplus
extern "C" {
#endif

void ra_encoder_init(struct ra_context* ctx, const ra_word_t* packet);

/* call this ra_code_length times to get all code words */
ra_word_t ra_encoder_next(struct ra_context* ctx);

/* this calls the above two functions */
void ra_encoder(struct ra_context* ctx, const ra_word_t* packet, ra_word_t* output);

#ifdef __cplusplus
}
#endif

#endif //__RA_ENCODER_H__
