/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_KURTOSIS_H
#define INCLUDED_SATELLITES_KURTOSIS_H

#include <gnuradio/sync_decimator.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief Estimates the Kurtosis of a complex signal
 * \ingroup satellites
 *
 * \details
 * This block computes an unbiased estimate of the Kurtosis of a complex
 * signal for each block of M input samples. The block supports vectors,
 * in which case the Kurtosis is computed component-wise. This can be used
 * to compute spectral Kurtosis, for instance.
 */
class SATELLITES_API kurtosis : virtual public gr::sync_decimator
{
public:
    typedef std::shared_ptr<kurtosis> sptr;

    /*!
     * \brief Build the Kurtosis block.
     *
     * \param block_size The block size to use to compute the Kurtosis estimate
     * \param vlen Vector length
     */
    static sptr make(size_t block_size, size_t vlen = 1);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_KURTOSIS_H */
