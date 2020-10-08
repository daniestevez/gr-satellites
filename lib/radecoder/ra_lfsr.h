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

#ifndef RA_LFSR_H
#define RA_LFSR_H

#include "ra_config.h"

#ifdef __cplusplus
extern "C" {
#endif

void ra_lfsr_init(struct ra_context* ctx, uint8_t seqno);
ra_index_t ra_lfsr_next(struct ra_context* ctx);
ra_index_t ra_lfsr_prev(struct ra_context* ctx);

#ifdef __cplusplus
}
#endif

#endif // RA_LFSR_H
