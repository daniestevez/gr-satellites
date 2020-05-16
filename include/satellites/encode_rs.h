/* -*- c++ -*- */
/*
 * Copyright 2018 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_ENCODE_RS_H
#define INCLUDED_SATELLITES_ENCODE_RS_H

#include <satellites/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace satellites {

    /*!
     * \brief <+description of block+>
     * \ingroup satellites
     *
     */
    class SATELLITES_API encode_rs : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<encode_rs> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of satellites::encode_rs.
       *
       * To avoid accidental use of raw pointers, satellites::encode_rs's
       * constructor is in a private implementation
       * class. satellites::encode_rs::make is the public interface for
       * creating new instances.
       */
      static sptr make(int basis);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_ENCODE_RS_H */

