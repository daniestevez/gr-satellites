/* -*- c++ -*- */
/*
 * Copyright 2020 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_NRZI_DECODE_H
#define INCLUDED_SATELLITES_NRZI_DECODE_H

#include <satellites/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace satellites {

    /*!
     * \brief NRZI decode
     * \ingroup satellites
     *
     */
    class SATELLITES_API nrzi_decode : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<nrzi_decode> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of satellites::nrzi_decode.
       *
       * To avoid accidental use of raw pointers, satellites::nrzi_decode's
       * constructor is in a private implementation
       * class. satellites::nrzi_decode::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_NRZI_DECODE_H */

