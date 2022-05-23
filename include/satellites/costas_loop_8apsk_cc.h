/* -*- c++ -*- */
/*
 * Copyright 2022 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_COSTAS_LOOP_8APSK_CC_H
#define INCLUDED_SATELLITES_COSTAS_LOOP_8APSK_CC_H

#include <gnuradio/blocks/control_loop.h>
#include <gnuradio/sync_block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief 8APSK Costas Loop
 * \ingroup satellites
 *
 */
class SATELLITES_API costas_loop_8apsk_cc : virtual public gr::sync_block,
                                            virtual public blocks::control_loop
{
public:
    typedef boost::shared_ptr<costas_loop_8apsk_cc> sptr;

    /*!
     * Make an 8APSK Costas Loop block.
     *
     * \param loop_bw internal 2nd order loop bandwidth
     */
    static sptr make(float loop_bw);

    /*!
     * Returns the current value of the loop error.
     */
    virtual float error() const = 0;
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_COSTAS_LOOP_8APSK_CC_H */
