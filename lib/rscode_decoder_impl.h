/* -*- c++ -*- */
/* 
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>.
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

#ifndef INCLUDED_SATELLITES_RSCODE_DECODER_IMPL_H
#define INCLUDED_SATELLITES_RSCODE_DECODERR_IMPL_H

#include <satellites/rscode_decoder.h>
#include <pmt/pmt.h>

#include <stdint.h>

#define RS_LEN 255

namespace gr {
  namespace satellites {

    class rscode_decoder_impl : public rscode_decoder
    {
     private:
      int d_npar;
      
     public:
      rscode_decoder_impl(int npar);
      ~rscode_decoder_impl();

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

#endif /* INCLUDED_SATELLITES_RSCODE_DECODER_IMPL_H */

