/*
 * K=7 r=1/2 Viterbi decoder in portable C
 * Copyright Feb 2004, Phil Karn, KA9Q
 * May be used under the terms of the GNU Lesser General Public License (LGPL)
 */

#ifndef VITERBI_H_
#define VITERBI_H_

#include <stdint.h>

#define VITERBI_CONSTRAINT	7
#define VITERBI_TAIL		1
#define VITERBI_RATE		2

/* r=1/2 k=7 convolutional encoder polynomials
 * The NASA-DSN convention is to use V27POLYA inverted, then V27POLYB
 * The CCSDS/NASA-GSFC convention is to use V27POLYB, then V27POLYA inverted
 */
#define	V27POLYA	0x6d
#define	V27POLYB	0x4f

void *create_viterbi_packed(int16_t len);
int init_viterbi_packed(void *vp,int starting_state);
int update_viterbi_packed(void *vp, unsigned char sym[], uint16_t npairs);
int chainback_viterbi_packed(void *vp, unsigned char *data, unsigned int nbits,unsigned int endstate);
void delete_viterbi_packed(void *vp);
void encode_viterbi_packed(unsigned char * channel, unsigned char * data, int framebits);
void set_viterbi_polynomial_packed(int16_t polys[2]);

#endif // VITERBI_H_
