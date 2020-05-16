/* -*- c++ -*- */
/*
 * Copyright 2016 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_U482C_DECODE_H
#define INCLUDED_SATELLITES_U482C_DECODE_H

#include <satellites/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace satellites {

    /*!
     * \brief <+description of block+>
     * \ingroup satellites
     *
     */
    class SATELLITES_API u482c_decode : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<u482c_decode> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of satellites::u482c_decode.
       *
       * To avoid accidental use of raw pointers, satellites::u482c_decode's
       * constructor is in a private implementation
       * class. satellites::u482c_decode::make is the public interface for
       * creating new instances.
       */
      static sptr make(bool verbose, int viterbi, int scrambler, int rs);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_U482C_DECODE_H */

