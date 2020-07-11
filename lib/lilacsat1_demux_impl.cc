/* -*- c++ -*- */
/*
 * Copyright 2017,2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <vector>
#include <cassert>
#include <cstring>

#include <gnuradio/io_signature.h>
#include "lilacsat1_demux_impl.h"

#define CODEC2_FRAME_LEN 7
#define CHUNK_LEN 24
#define BITS_PER_BYTE 8
#define PACKET_LEN 116
#define HEADER_LEN 4
#define FRAME_LEN (5 * (CHUNK_LEN - CODEC2_FRAME_LEN) - HEADER_LEN)

namespace gr {
  namespace satellites {

    lilacsat1_demux::sptr
    lilacsat1_demux::make(std::string tag)
    {
      return gnuradio::get_initial_sptr
        (new lilacsat1_demux_impl(tag));
    }

    /*
     * The private constructor
     */
    lilacsat1_demux_impl::lilacsat1_demux_impl(std::string tag)
      : gr::sync_block("lilacsat1_demux",
              gr::io_signature::make(1, 1, sizeof(uint8_t)),
              gr::io_signature::make(0, 0, 0))
    {
      d_position = -1;
      d_tag = pmt::string_to_symbol(tag);
      d_frame = new uint8_t[FRAME_LEN];
      memset(d_frame, 0, FRAME_LEN);
      d_codec2 = new uint8_t[CODEC2_FRAME_LEN];
      memset(d_codec2, 0, CODEC2_FRAME_LEN);

      message_port_register_out(pmt::mp("frame"));
      message_port_register_out(pmt::mp("codec2"));
    }

    /*
     * Our virtual destructor.
     */
    lilacsat1_demux_impl::~lilacsat1_demux_impl()
    {
      delete[] d_frame;
    }

    int
    lilacsat1_demux_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      int i;
      const uint8_t *in = (const uint8_t *) input_items[0];
      std::vector<tag_t> tags;

      for (i = 0; i < noutput_items; i++) {
	get_tags_in_window(tags, 0, i, i+1, d_tag);

	if (!tags.empty()) {
	  d_position = 0;
	}

	if (d_position == PACKET_LEN*BITS_PER_BYTE) {
	  d_position = -1;

	  message_port_pub(pmt::mp("frame"),
			   pmt::cons(pmt::PMT_NIL,
				     pmt::init_u8vector(FRAME_LEN, d_frame)));
	  memset(d_frame, 0, FRAME_LEN);
	}

	if (d_position == -1) continue;

	int base = d_position/BITS_PER_BYTE + HEADER_LEN;
	int bit = BITS_PER_BYTE - 1 - d_position % BITS_PER_BYTE;
	int idx = base % CHUNK_LEN;
	if (idx >= CHUNK_LEN - CODEC2_FRAME_LEN) {
	  int byte = idx - (CHUNK_LEN - CODEC2_FRAME_LEN);
	  assert(byte < CODEC2_FRAME_LEN);
	  d_codec2[byte] |= (in[i] & 1) << bit;

	  if ((byte == CODEC2_FRAME_LEN - 1) && (bit == 0)) {
	    message_port_pub(pmt::mp("codec2"),
			     pmt::cons(pmt::PMT_NIL,
				       pmt::init_u8vector(CODEC2_FRAME_LEN, d_codec2)));
	    memset(d_codec2, 0, CODEC2_FRAME_LEN);
	  }
	}
	else if (idx < CHUNK_LEN - CODEC2_FRAME_LEN) {
	  int byte = (base / CHUNK_LEN) * (CHUNK_LEN - CODEC2_FRAME_LEN) + idx - HEADER_LEN;
	  assert(byte < FRAME_LEN);
	  d_frame[byte] |= (in[i] & 1) << bit;
	}

	d_position++;
      }

      return i;
    }

  } /* namespace satellites */
} /* namespace gr */

