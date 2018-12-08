/* -*- c++ -*- */
/* 
 * Copyright 2018 Daniel Estevez <daniel@destevez.net>.
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

#ifndef INCLUDED_SATELLITES_DECODE_RS_GENERAL_H
#define INCLUDED_SATELLITES_DECODE_RS_GENERAL_H

#include <satellites/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace satellites {

    /*!
     * \brief <+description of block+>
     * \ingroup satellites
     *
     */
    class SATELLITES_API decode_rs_general : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<decode_rs_general> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of satellites::decode_rs_general.
       *
       * To avoid accidental use of raw pointers, satellites::decode_rs_general's
       * constructor is in a private implementation
       * class. satellites::decode_rs_general::make is the public interface for
       * creating new instances.
       */
      static sptr make(int gfpoly, int fcr, int prim, int nroots, bool verbose);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_DECODE_RS_GENERAL_H */

