/*
 * K=7 r=1/2 Viterbi decoder in portable C
 * Copyright Feb 2004, Phil Karn, KA9Q
 * May be used under the terms of the GNU Lesser General Public License (LGPL)
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <limits.h>

#include "viterbi.h"

#ifndef BITS_PER_BYTE
#define BITS_PER_BYTE 8
#endif

#ifdef __GNUC__
#define likely(x)       __builtin_expect((x),1)
#define unlikely(x)     __builtin_expect((x),0)
#else
#define likely(x)       (x)
#define unlikely(x)     (x)
#endif

#define get_bit(_p, _n) (_p[(_n) / (uint8_t)BITS_PER_BYTE] >> ((uint8_t)BITS_PER_BYTE - 1 - ((_n) % (uint8_t)BITS_PER_BYTE)) & (uint8_t)0x01)

typedef union { uint8_t w[64]; } metric_t;
typedef union { uint8_t w[8];} decision_t;
typedef union { uint8_t c[32]; } branchtab_t;

/* We use the CCSDS convention 
 * (see CCSDS 131.0-B-2 TM Synchronization and Channel Coding p3-2) */
static int16_t polys[2] = {V27POLYB, -V27POLYA};
static bool init = false;

static uint8_t partab[256];
static bool p_init;

/* State info for Viterbi decoder instance */
struct v27 {
    metric_t metrics1;                  /* path metric buffer 1 */
    metric_t metrics2;                  /* path metric buffer 2 */
    decision_t *dp;                     /* Pointer to current decision */
    metric_t *old_metrics,*new_metrics; /* Pointers to path metrics, swapped on every bit */
    decision_t *decisions;              /* Beginning of decisions for block */
    uint16_t dlen;                      /* Length of decisions array for block */
};

static branchtab_t branchtab[2];
static struct v27 v27_local;
static decision_t decisions_local;

/* Create 256-entry odd-parity lookup table */
static void partab_init(void)
{
    int i, cnt, ti;

    /* Initialize parity lookup table */
    for (i = 0; i < 256; i++) {
        cnt = 0;
        ti = i;
        while (ti) {
            if (ti & 1)
                cnt++;
            ti >>= 1;
        }
        partab[i] = cnt & 1;
    }

    p_init = true;
}

static inline int parityb(unsigned char x)
{
    extern uint8_t partab[256];
    extern bool p_init;

    if (!p_init)
        partab_init();

    return partab[x];
}

static inline int parity(uint32_t x)
{
    /* Fold down to one byte */
    x ^= (x >> 16);
    x ^= (x >> 8);

    return parityb(x);
}

/* Initialize Viterbi decoder for start of new frame */
int init_viterbi_packed(void *p, int starting_state)
{
    struct v27 *vp = p;
    int i;

    if (p == NULL)
        return -1;

    for (i = 0; i < 64; i++)
        vp->metrics1.w[i] = 63;

    vp->old_metrics = &vp->metrics1;
    vp->new_metrics = &vp->metrics2;
    vp->dp = vp->decisions;
    vp->old_metrics->w[starting_state & 63] = 0; /* Bias known start state */
    
    return 0;
}

void set_viterbi_polynomial_packed(int16_t polys[2])
{
    int state;

    for (state = 0; state < 32; state++) {
        branchtab[0].c[state] = (polys[0] < 0) ^ parity((2 * state) & abs(polys[0])) ? 1 : 0;
        branchtab[1].c[state] = (polys[1] < 0) ^ parity((2 * state) & abs(polys[1])) ? 1 : 0;
    }

    init = true;
}

/* Create a new instance of a Viterbi decoder */
void *create_viterbi_packed(int16_t len)
{
    /* Keep state in internal RAM */
    struct v27 *vp = &v27_local;

    if (!init)
        set_viterbi_polynomial_packed(polys);

    vp->dlen = (len + 6) * sizeof(decision_t);
    if ((vp->decisions = malloc(vp->dlen)) == NULL)
        return NULL;

    init_viterbi_packed(vp, 0);

    return vp;
}

/* Viterbi chainback */
int chainback_viterbi_packed(void *p, unsigned char *data, unsigned int nbits, unsigned int endstate)
{
    int k;
    struct v27 *vp = p;
    decision_t *d;
    int errors = vp->old_metrics->w[endstate];

    if (unlikely(p == NULL))
        return -1;

    d = vp->decisions;

    /* Make room beyond the end of the encoder register so we can
     * accumulate a full byte of decoded data */
    endstate %= 64;
    endstate <<= 2;

    /* The store into data[] only needs to be done every 8 bits.
     * But this avoids a conditional branch, and the writes will
     * combine in the cache anyway (no they wont because we have
     * a crappy AVR, but nevermind ...) */
    d += VITERBI_CONSTRAINT - 1; // Look past tail
    while (likely(nbits--)) {
        k = (d[nbits].w[(endstate >> 2) / 8] >> ((endstate >> 2) & 7)) & 1;
        data[nbits >> 3] = endstate = (endstate >> 1) | (k << 7);
    }

    return errors;
}

/* Delete instance of a Viterbi decoder */
void delete_viterbi(void *p)
{
    struct v27 *vp = p;

    if (vp->decisions != NULL)
        free((void*)vp->decisions);
}

/* C-language butterfly */
#define BFLY(b)                                                             \
    do {                                                                    \
        metric = (branchtab[0].c[b] ^ sym0) + (branchtab[1].c[b] ^ sym1);   \
                                                                            \
        m0 = vp->old_metrics->w[b] + metric;                                \
        m1 = vp->old_metrics->w[b + 32] + (2 - metric);                     \
        decision = m0 > m1;                                                 \
        vp->new_metrics->w[(b << 1)] = decision ? m1 : m0;                  \
        d->w[b >> 2] |= decision << (((b << 1)) & 7);                       \
                                                                            \
        m0 -= (metric + metric - 2);                                        \
        m1 += (metric + metric - 2);                                        \
        decision = m0 > m1;                                                 \
        vp->new_metrics->w[(b << 1) + 1] = decision ? m1 : m0;              \
        d->w[b >> 2] |= decision << (((b << 1) + 1) & 7);                   \
    } while (0)

/* 
 * Update decoder with a block of demodulated symbols
 * Note that nbits is the number of decoded data bits, not the number
 * of symbols!
 */
int update_viterbi_packed(void *p, uint8_t *syms, uint16_t nbits)
{
    struct v27 *vp = p;
    void *tmp;
    decision_t *dp, *d = &decisions_local;
    uint16_t i = 0;
    uint8_t m0, m1, decision, metric, sym0, sym1;

    if (unlikely(p == NULL))
        return -1;

    dp = vp->dp;

    while (likely(nbits--)) {
        /* Cache decisions in internal memory */
        memset(d, 0, sizeof(decision_t));

        /* Read symbols */
        sym0 = get_bit(syms, i);
        sym1 = get_bit(syms, i + 1); 
        i += 2;

        /* Unrolled butterflies */
        BFLY(0);
        BFLY(1);
        BFLY(2);
        BFLY(3);
        BFLY(4);
        BFLY(5);
        BFLY(6);
        BFLY(7);
        BFLY(8);
        BFLY(9);
        BFLY(10);
        BFLY(11);
        BFLY(12);
        BFLY(13);
        BFLY(14);
        BFLY(15);
        BFLY(16);
        BFLY(17);
        BFLY(18);
        BFLY(19);
        BFLY(20);
        BFLY(21);
        BFLY(22);
        BFLY(23);
        BFLY(24);
        BFLY(25);
        BFLY(26);
        BFLY(27);
        BFLY(28);
        BFLY(29);
        BFLY(30);
        BFLY(31);

        /* Writeback cached data */
        memcpy(dp++, d, sizeof(decision_t));

        /* Swap pointers to old and new metrics */
        tmp = vp->old_metrics;
        vp->old_metrics = vp->new_metrics;
        vp->new_metrics = tmp;
    }

    vp->dp = d;
    return 0;
}

void encode_viterbi_packed(unsigned char *channel, unsigned char *data, int framebits)
{
    int i;
    unsigned char bit;
    unsigned char in_sr = 0;
    unsigned char out_sr = 0;
    unsigned char temp[256];

    for (i = 0; i < framebits + 8; i++) {
        bit = (i >= framebits) ? 0 : get_bit(data, i);

        in_sr = (in_sr << 1) | bit;
        out_sr = (out_sr << 1) | ((polys[0] < 0) ^ parity(in_sr & abs(polys[0])));
        out_sr = (out_sr << 1) | ((polys[1] < 0) ^ parity(in_sr & abs(polys[1])));
        temp[i>>2] = out_sr;
    }

    memcpy(channel, temp, 2 * (framebits / 8) + 2);
}
