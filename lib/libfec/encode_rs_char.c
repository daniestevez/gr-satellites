/* Reed-Solomon encoder
 * Copyright 2002, Phil Karn, KA9Q
 * May be used under the terms of the GNU Lesser General Public License (LGPL)
 */
#include <string.h>

#include "char.h"
#include "rs-common.h"

void encode_rs_char(void *p,data_t *data, data_t *parity){
  struct rs *rs = (struct rs *)p;

#include "encode_rs.h"

}
