/* This function wraps around the fixed 8-bit decoder, performing the
 * basis transformations necessary to meet the CCSDS standard
 *
 * Copyright 2002, Phil Karn, KA9Q
 * May be used under the terms of the GNU Lesser General Public License (LGPL)
 */
#include "ccsds.h"
#include "fec.h"

int decode_rs_ccsds(data_t *data,int *eras_pos,int no_eras,int pad){
  int i,r;
  data_t cdata[NN];

  /* Convert data from dual basis to conventional */
  for(i=0;i<NN-pad;i++)
    cdata[i] = Tal1tab[data[i]];

  r = decode_rs_8(cdata,eras_pos,no_eras,pad);

  if(r > 0){
    /* Convert from conventional to dual basis */
    for(i=0;i<NN-pad;i++)
      data[i] = Taltab[cdata[i]];
  }
  return r;
}
