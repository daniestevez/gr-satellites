/* General purpose Reed-Solomon decoder for 8-bit symbols or less
 * Copyright 2003 Phil Karn, KA9Q
 * May be used under the terms of the GNU Lesser General Public License (LGPL)
 */

#ifdef DEBUG
#include <stdio.h>
#endif

#include <string.h>

#include "fixed.h"

int decode_rs_8(data_t *data, int *eras_pos, int no_eras, int pad){
  int retval;
 
  if(pad < 0 || pad > 222){
    return -1;
  }

#include "decode_rs.h"
  
  return retval;
}
