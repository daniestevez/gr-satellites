/* -*- c++ -*- */
/*
 * Copyright 2019 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "distributed_syncframe_soft_impl.h"

namespace gr {
  namespace satellites {

    distributed_syncframe_soft::sptr
    distributed_syncframe_soft::make(int threshold, const std::string& syncword, int step)
    {
      return gnuradio::get_initial_sptr
        (new distributed_syncframe_soft_impl(threshold, syncword, step));
    }

    /*
     * The private constructor
     */
    distributed_syncframe_soft_impl::distributed_syncframe_soft_impl(int threshold, const std::string& syncword, int step)
      : gr::sync_block("distributed_syncframe_soft",
              gr::io_signature::make(1, 1, sizeof(float)),
	      gr::io_signature::make(0, 0, 0)),
	d_threshold(threshold),
	d_step(step)
    {
      // look at LSB only, as in correlate_access_code_bb_impl.cc
      for (auto s : syncword) d_syncword.push_back(s & 1);
            
      set_history(d_syncword.size() * d_step);

      message_port_register_out(pmt::mp("out"));
    }

    /*
     * Our virtual destructor.
     */
    distributed_syncframe_soft_impl::~distributed_syncframe_soft_impl()
    {
    }

    int
    distributed_syncframe_soft_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      int match;

      const float *in = (const float *) input_items[0];

      for (int i = 0; i < noutput_items; i++) {
	match = 0;
	for (int j = 0; j < d_syncword.size(); j++) {
	  match += (in[i + j * d_step] < 0.0) ^ d_syncword[j];
	}
	if (match >= d_syncword.size() - d_threshold) {
	  // sync found
	  message_port_pub(pmt::mp("out"),
			   pmt::cons(pmt::PMT_NIL,
				     pmt::init_f32vector(d_syncword.size() * d_step, in + i)));
	}
      }

      return noutput_items;
    }

  } /* namespace satellites */
} /* namespace gr */

