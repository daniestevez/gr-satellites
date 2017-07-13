/*
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/*
 This algorithm is based on 
 R.H. Morelos-Zaragoza, The Art of Error Correcting Coding, Wiley, 2002; Section 2.2.3
*/

#ifndef _GOLAY24_H
#define _GOLAY24_H

#include <stdint.h>

int decode_golay24(uint32_t *data);
int encode_golay24(uint32_t *data);

#endif
