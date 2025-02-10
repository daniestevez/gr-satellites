/* -*- c++ -*- */
/*
 * Copyright 2018,2020,2024 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_ENCODE_RS_H
#define INCLUDED_SATELLITES_ENCODE_RS_H

#include <gnuradio/sync_block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief Reed-Solomon encoder
 * \ingroup satellites
 *
 */
class SATELLITES_API encode_rs : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<encode_rs> sptr;

    /*!
     * \brief Constructs a CCSDS Reed Solomon encoder using PDU IO.
     *
     * \param dual_basis Selects the dual or conventional basis.
     * \param interleave Interleave depth.
     */
    static sptr make(bool dual_basis, int interleave = 1);

    /*!
     * \brief Constructs a CCSDS Reed Solomon encoder using vector stream IO.
     *
     * \param frame_size Input frame size.
     * \param dual_basis Selects the dual or conventional basis.
     * \param interleave Interleave depth.
     */
    static sptr make(int frame_size, bool dual_basis, int interleave = 1);

    /*!
     * \brief Constructs a generic Reed Solomon encoder using PDU IO.
     *
     * \param symsize Size of the finite field elements.
     * \param gfpoly Polynomial defining the finite field.
     * \param fcr First consecutive root of the Reed-Solomon generator polynomial.
     * \param prim Primitive element used in the generator polynomial.
     * \param nroots Number of roots of the generator polynomial.
     * \param interleave Interleave depth.
     */
    static sptr
    make(int symsize, int gfpoly, int fcr, int prim, int nroots, int interleave = 1);

    /*!
     * \brief Constructs a generic Reed Solomon encoder using vector stream IO.
     *
     * \param frame_size Input frame size.
     * \param symsize Size of the finite field elements.
     * \param gfpoly Polynomial defining the finite field.
     * \param fcr First consecutive root of the Reed-Solomon generator polynomial.
     * \param prim Primitive element used in the generator polynomial.
     * \param nroots Number of roots of the generator polynomial.
     * \param interleave Interleave depth.
     */
    static sptr make(int frame_size,
                     int symsize,
                     int gfpoly,
                     int fcr,
                     int prim,
                     int nroots,
                     int interleave);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_ENCODE_RS_H */
