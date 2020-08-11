/* Stuff specific to the CCSDS (255,223) RS codec
 * (255,223) code over GF(256). Note: the conventional basis is still
 * used; the dual-basis mappings are performed in [en|de]code_rs_ccsds.c
 *
 * Copyright 2003 Phil Karn, KA9Q
 * May be used under the terms of the GNU Lesser General Public License (LGPL)
 */
typedef unsigned char data_t;

static inline int mod255(int x){
  while (x >= 255) {
    x -= 255;
    x = (x >> 8) + (x & 255);
  }
  return x;
}
#define MODNN(x) mod255(x)

extern data_t CCSDS_alpha_to[];
extern data_t CCSDS_index_of[];
extern data_t CCSDS_poly[];

#define MM 8
#define NN 255
#define ALPHA_TO CCSDS_alpha_to
#define INDEX_OF CCSDS_index_of
#define GENPOLY CCSDS_poly
#define NROOTS 32
#define FCR 112
#define PRIM 11
#define IPRIM 116
#define PAD pad

