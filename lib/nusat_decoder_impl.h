/* -*- c++ -*- */
/*
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_NUSAT_DECODER_IMPL_H
#define INCLUDED_SATELLITES_NUSAT_DECODERR_IMPL_H

#include <satellites/nusat_decoder.h>
#include <pmt/pmt.h>

#include <stdint.h>

#define MSG_LEN 64
#define HEADER_LEN 2
#define LEN_BYTE 0
#define CRC_BYTE 1

namespace gr {
  namespace satellites {

    class nusat_decoder_impl : public nusat_decoder
    {
     private:
      static const uint8_t d_scrambler_sequence[];
      static const uint_fast8_t crc8_table[];
      void *d_rs;
      uint_fast8_t crc8(const uint8_t *data, size_t data_len);
      
     public:
      nusat_decoder_impl();
      ~nusat_decoder_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

      void msg_handler (pmt::pmt_t pmt_msg);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_NUSAT_DECODER_IMPL_H */

