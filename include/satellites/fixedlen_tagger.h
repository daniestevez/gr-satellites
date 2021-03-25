/* -*- c++ -*- */
/*
 * Copyright 2021 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_FIXEDLEN_TAGGER_H
#define INCLUDED_SATELLITES_FIXEDLEN_TAGGER_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief NRZI encode
 * \ingroup satellites
 *
 */
class SATELLITES_API fixedlen_tagger : virtual public gr::block
{
public:
    typedef boost::shared_ptr<fixedlen_tagger> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of satellites::fixedlen_tagger.
     *
     * To avoid accidental use of raw pointers, satellites::fixedlen_tagger's
     * constructor is in a private implementation
     * class. satellites::fixedlen_tagger::make is the public interface for
     * creating new instances.
     */
    static sptr make(size_t sizeof_stream_item,
                     const std::string& syncword_tag,
                     const std::string& packetlen_tag,
                     size_t packet_len);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_FIXEDLEN_TAGGER_H */
