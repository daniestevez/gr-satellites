/* -*- c++ -*- */
/* 
 * Copyright 2019 Daniel Estevez <daniel@destevez.net>.
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

#ifndef INCLUDED_SATELLITES_DECODE_RA_CODE_IMPL_H
#define INCLUDED_SATELLITES_DECODE_RA_CODE_IMPL_H

#include <satellites/decode_ra_code.h>

extern "C" {
#include "radecoder/ra_config.h"
}

namespace gr {
  namespace satellites {

    class decode_ra_code_impl : public decode_ra_code
    {
     private:
      int d_size;
      struct ra_context *d_ra_context;
      
     public:
      decode_ra_code_impl(int size);
      ~decode_ra_code_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

      void msg_handler(pmt::pmt_t pmt_msg);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_DECODE_RA_CODE_IMPL_H */

