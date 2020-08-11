/* This function wraps around the fixed 8-bit encoder, performing the
 * basis transformations necessary to meet the CCSDS standard
 *
 * Copyright 2002, Phil Karn, KA9Q
 * fixed bug Aug 2007
 * May be used under the terms of the GNU Lesser General Public License (LGPL)
 */
#include "ccsds.h"
#include "fec.h"

void encode_rs_ccsds(data_t *data,data_t *parity,int pad){
  int i;
  data_t cdata[NN-NROOTS];

  /* Convert data from dual basis to conventional */
  for(i=0;i<NN-NROOTS-pad;i++)
    cdata[i] = Tal1tab[data[i]];

  encode_rs_8(cdata,parity,pad);

  /* Convert parity from conventional to dual basis */
  for(i=0;i<NROOTS;i++)
    parity[i] = Taltab[parity[i]];
}
