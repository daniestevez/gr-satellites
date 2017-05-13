/*
 * Copyright (c) 2008 Johan Christiansen
 * Copyright (c) 2012 Jeppe Ledet-Pedersen <jlp@satlab.org>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include <stdio.h>
#include <string.h>

void ccsds_generate_sequence(char *sequence, int length)
{
	char x[9] = {1, 1, 1, 1, 1, 1, 1, 1, 1};
	int i;

	/* Generate the sequence */
	memset(sequence, 0, length);

	/* The pseudo random sequence shall be generated using the polynomial
	 * h(x) = x8 + x7 + x5 + x3 + 1 */
	for (i = 0; i < length*8; i++) {
		sequence[i/8] = sequence[i/8] | x[1] << 7 >> (i%8);
		x[0] = (x[8] + x[6] + x[4] + x[1]) % 2;
		x[1] = x[2];
		x[2] = x[3];
		x[3] = x[4];
		x[4] = x[5];
		x[5] = x[6];
		x[6] = x[7];
		x[7] = x[8];
		x[8] = x[0];
	}
}

void ccsds_xor_sequence(unsigned char *data, char *sequence, int length)
{
	int i;

	for (i = 0; i < length; i++)
		data[i] ^= sequence[i];
}
