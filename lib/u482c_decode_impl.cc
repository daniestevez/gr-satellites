/* -*- c++ -*- */
/*
 * Copyright 2016 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <algorithm>

#include <cstdio>

#include <new>
#include <utility>

#include <gnuradio/io_signature.h>
#include "u482c_decode_impl.h"

extern "C" {
#include "libfec/fec.h"
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
	      gr::io_signature::make(0, 0, 0)),
	d_verbose(verbose),
	d_viterbi(viterbi),
	d_scrambler(scrambler),
	d_rs(rs)
    {
      // init FEC
      if (d_viterbi != OFF) {
	int16_t polys[2] = {V27POLYA, V27POLYB};
	set_viterbi_polynomial_packed(polys);
	d_vp = create_viterbi_packed(d_rs_len * 8);
	if (!d_vp) throw std::bad_alloc();
      }

      if (d_scrambler != OFF) {
	ccsds_generate_sequence(d_ccsds_sequence.data(), d_ccsds_sequence.size());
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
      if (d_vp) delete_viterbi_packed(d_vp);
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
      size_t length(0);
      auto msg = pmt::u8vector_elements(pmt::cdr(pmt_msg), length);

      auto data_len = std::min(length, d_data.size());
      memcpy(d_data.data(), msg, data_len);

      // decode length field
      uint32_t length_field = (d_data[0] << 16) | (d_data[1] << 8) | d_data[2];
      auto golay_res = decode_golay24(&length_field);
      if (golay_res < 0) {
	if (d_verbose) {
	  std::printf("Golay decode failed.\n");
	}
	return;
      }

      auto frame_len = length_field & 0xff;
      bool viterbi_flag = length_field & 0x100;
      bool scrambler_flag = length_field & 0x200;
      bool rs_flag = length_field & 0x400;

      if (d_verbose) {
	std::printf("Golay decode OK. Bit errors: %d, Frame length: %d, Viterbi: %d, Scrambler %d, Reed-Solomon: %d.\n",
		    golay_res, frame_len, viterbi_flag, scrambler_flag, rs_flag);
      }

      size_t rx_len;
      auto packet = &d_data[d_header_len];
      // Viterbi decoding
      if ((d_viterbi == ON) || (d_viterbi == AUTO && viterbi_flag)) {
	rx_len = frame_len / VITERBI_RATE - VITERBI_TAIL;
	if (rx_len < 0) {
	  if (d_verbose) {
	    std::printf("Frame too short for Viterbi decoder.\n");
	  }
	  return;
	}
	init_viterbi_packed(d_vp, 0);
	update_viterbi_packed(d_vp, packet, rx_len * 8 + VITERBI_CONSTRAINT - 1);
	auto viterbi_res = chainback_viterbi_packed(d_vp, packet, rx_len * 8, 0);
	if (d_verbose) {
	  std::printf("Viterbi decode bit errors: %d\n", viterbi_res);
	}
      }
      else {
	rx_len = frame_len;
      }

      // Descrambling
      if ((d_scrambler == ON) || (d_scrambler == AUTO && scrambler_flag)) {
	ccsds_xor_sequence(packet, d_ccsds_sequence.data(), rx_len);
      }
      
      // RS decoding
      if ((d_rs == ON) || (d_rs == AUTO && rs_flag)) {
	auto rs_res = decode_rs_8(packet, NULL, 0, RS_LEN - rx_len);
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
      std::swap(packet[0], packet[3]);
      std::swap(packet[1], packet[2]);

      // Send by GNUradio message
      message_port_pub(pmt::mp("out"),
		       pmt::cons(pmt::PMT_NIL,
				 pmt::init_u8vector(rx_len, packet)));
    }
  } /* namespace satellites */
} /* namespace gr */

