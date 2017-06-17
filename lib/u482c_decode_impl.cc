/* -*- c++ -*- */
/* 
 * Copyright 2016 Daniel Estevez <daniel@destevez.net>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <cstdio>

#include <gnuradio/io_signature.h>
#include "u482c_decode_impl.h"

extern "C" {
#include <fec.h>
#include "randomizer.h"
#include "golay24.h"
#include "viterbi.h"
}

#define AUTO -1
#define OFF 0
#define ON 1

namespace gr {
  namespace satellites {

    u482c_decode::sptr
    u482c_decode::make(bool verbose, int viterbi, int scrambler, int rs)
    {
      return gnuradio::get_initial_sptr
        (new u482c_decode_impl(verbose, viterbi, scrambler, rs));
    }

    /*
     * The private constructor
     */
    u482c_decode_impl::u482c_decode_impl(bool verbose, int viterbi, int scrambler, int rs)
      : gr::block("u482c_decode",
              gr::io_signature::make(0, 0, 0),
	      gr::io_signature::make(0, 0, 0))
    {
      int16_t polys[2] = {V27POLYA, V27POLYB};
      d_verbose = verbose;
      d_viterbi = viterbi;
      d_scrambler = scrambler;
      d_rs = rs;

      // init FEC
      if (d_viterbi != OFF) {
	set_viterbi_polynomial_packed(polys);
	d_vp = create_viterbi_packed(RS_LEN * 8);
      }

      if (d_scrambler != OFF) {
	ccsds_generate_sequence(d_ccsds_sequence, RS_LEN);
      }
      
      message_port_register_out(pmt::mp("out"));
      message_port_register_in(pmt::mp("in"));
      set_msg_handler(pmt::mp("in"),
		      boost::bind(&u482c_decode_impl::msg_handler, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    u482c_decode_impl::~u482c_decode_impl()
    {
    }

    void
    u482c_decode_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
    }

    int
    u482c_decode_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      return 0;
    }

    void
    u482c_decode_impl::msg_handler (pmt::pmt_t pmt_msg) {
      pmt::pmt_t msg = pmt::cdr(pmt_msg);
      uint8_t data[HEADER_LEN + RS_LEN];
      uint8_t * const packet = data + HEADER_LEN;
      uint8_t tmp;
      int rs_res, viterbi_res, golay_res;
      int rx_len, frame_len = -1;
      size_t offset(0);
      register uint32_t length_field;
      bool viterbi_flag, scrambler_flag, rs_flag;
      bool doing_rs;
      int i;

      memcpy(data, pmt::uniform_vector_elements(msg, offset), sizeof(data));

      // decode length field
      length_field = (data[0] << 16) | (data[1] << 8) | data[2];
      golay_res = decode_golay24(&length_field);
      if (golay_res < 0) {
	if (d_verbose) {
	  std::printf("Golay decode failed.\n");
	}
	return;
      }

      frame_len = length_field & 0xff;
      viterbi_flag = length_field & 0x100;
      scrambler_flag = length_field & 0x200;
      rs_flag = length_field & 0x400;

      if (d_verbose) {
	std::printf("Golay decode OK. Bit errors: %d, Frame length: %d, Viterbi: %d, Scrambler %d, Reed-Solomon: %d.\n",
		    golay_res, frame_len, viterbi_flag, scrambler_flag, rs_flag);
      }

      // Viterbi decoding
      if ((d_viterbi == ON) || (d_viterbi == AUTO && viterbi_flag)) {
	rx_len = frame_len / VITERBI_RATE - VITERBI_TAIL;
	init_viterbi_packed(d_vp, 0);
	update_viterbi_packed(d_vp, packet, rx_len * 8 + VITERBI_CONSTRAINT - 1);
	viterbi_res = chainback_viterbi_packed(d_vp, packet, rx_len * 8, 0);
	if (d_verbose) {
	  std::printf("Viterbi decode bit errors: %d\n", viterbi_res);
	}
      }
      else {
	rx_len = frame_len;
      }

      // Descrambling
      if ((d_scrambler == ON) || (d_scrambler == AUTO && scrambler_flag)) {
	ccsds_xor_sequence(packet, d_ccsds_sequence, rx_len);
      }
      
      // RS decoding
      doing_rs = (d_rs == ON) || (d_rs == AUTO && rs_flag);
      if (doing_rs) {
	rs_res = decode_rs_8(packet, NULL, 0, RS_LEN - rx_len);
	rx_len -= 32;

	if (rs_res < 0) {
	  if (d_verbose) {
	    std::printf("RS decode failed.\n");
	  }
	  return;
	}

	if (d_verbose) {
	  std::printf("RS decode OK. Byte errors: %d.\n", rs_res);
	}
      }

      // Send via GNU Radio message
      // Swap CSP header
      tmp = packet[0];
      packet[0] = packet[3];
      packet[3] = tmp;
      tmp = packet[1];
      packet[1] = packet[2];
      packet[2] = tmp;

      // Send by GNUradio message
      message_port_pub(pmt::mp("out"),
		       pmt::cons(pmt::PMT_NIL,
				 pmt::init_u8vector(rx_len, packet)));
    }
  } /* namespace satellites */
} /* namespace gr */

