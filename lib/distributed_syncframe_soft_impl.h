/* -*- c++ -*- */
/*
 * Copyright 2019 Daniel Estevez <daniel@destevez.net>.
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

#ifndef INCLUDED_SATELLITES_DISTRIBUTED_SYNCFRAME_SOFT_IMPL_H
#define INCLUDED_SATELLITES_DISTRIBUTED_SYNCFRAME_SOFT_IMPL_H

#include <satellites/distributed_syncframe_soft.h>

namespace gr {
  namespace satellites {

    class distributed_syncframe_soft_impl : public distributed_syncframe_soft
    {
     private:
      int d_threshold;
      int d_synclen;
      int d_step;
      uint8_t *d_syncword;
            
     public:
      distributed_syncframe_soft_impl(int threshold, const std::string& syncword, int step);
      ~distributed_syncframe_soft_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_DISTRIBUTED_SYNCFRAME_SOFT_IMPL_H */
