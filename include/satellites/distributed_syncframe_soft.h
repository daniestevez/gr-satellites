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

#ifndef INCLUDED_SATELLITES_DISTRIBUTED_SYNCFRAME_SOFT_H
#define INCLUDED_SATELLITES_DISTRIBUTED_SYNCFRAME_SOFT_H

#include <satellites/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace satellites {

    /*!
     * \brief <+description of block+>
     * \ingroup satellites
     *
     */
    class SATELLITES_API distributed_syncframe_soft : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<distributed_syncframe_soft> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of satellites::distributed_syncframe_soft.
       *
       * To avoid accidental use of raw pointers, satellites::distributed_syncframe_soft's
       * constructor is in a private implementation
       * class. satellites::distributed_syncframe_soft::make is the public interface for
       * creating new instances.
       */
      static sptr make(int threshold, const std::string& syncword, int step);
    };

  } // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_DISTRIBUTED_SYNCFRAME_H */

