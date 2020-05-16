/* -*- c++ -*- */
/*
 * Copyright 2017 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_AO40_RS_DECODER_H
#define INCLUDED_SATELLITES_AO40_RS_DECODER_H

#include <satellites/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace satellites {

    /*!
     * \brief <+description of block+>
     * \ingroup satellites
     *
     */
    class SATELLITES_API ao40_rs_decoder : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<ao40_rs_decoder> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of satellites::ao40_rs_decoder.
       *
       * To avoid accidental use of raw pointers, satellites::ao40_rs_decoder's
       * constructor is in a private implementation
       * class. satellites::ao40_rs_decoder::make is the public interface for
       * creating new instances.
       */
      static sptr make(bool verbose);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_AO40_RS_DECODER_H */

