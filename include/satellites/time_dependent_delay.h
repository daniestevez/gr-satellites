/* -*- c++ -*- */
/*
 * Copyright 2025 Daniel Estevez <daniel@destevez.net>.
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SATELLITES_TIME_DEPENDENT_DELAY_H
#define INCLUDED_SATELLITES_TIME_DEPENDENT_DELAY_H

#include <gnuradio/sync_block.h>
#include <satellites/api.h>
#include <string>
#include <vector>

namespace gr {
namespace satellites {

/*!
 * \brief Applies a time-dependent group delay by using a delay vs. time textfile
 * \ingroup satellites
 *
 * \details
 * This block is similar to the Doppler Correction block, in the sense that
 * it uses a text file that lists a time series of delay vs. time. The format
 * of this text file is very similar to the one used by Doppler Correction.
 * Each line of the file contains a timestamp and a delay. The format of the
 * timestamp is the same as for Doppler correction. The delay is given in
 * seconds.
 *
 * Like the Doppler Correction block, this block can use time tags to update
 * its internal timestamp.
 *
 * The block interpolates the delay linearly for each sample, and uses a
 * polyphase filterbank to apply the appropriate delay.
 */
class SATELLITES_API time_dependent_delay : virtual public gr::sync_block
{
public:
    typedef boost::shared_ptr<time_dependent_delay> sptr;

    /*!
     * \brief Build the Time-dependent Delay block.
     *
     * \param filename Path of the text file describing the delay vs. time data
     * \param samp_rate Sample rate
     * \param t0 Timestamp corresponding to the first sample
     * \param taps Taps for the fractional delay polyphase filterbank
     * \param num_filters Number of filters in the polyphase filterbank
     */
    static sptr make(const std::string& filename,
                     double samp_rate,
                     double t0,
                     const std::vector<float>& taps,
                     int num_filters);

    /*!
     * \brief Sets the current time.
     *
     * \param t Tiemstamp corresponding to the current time.
     */
    virtual void set_time(double t) = 0;

    /*!
     * \brief Returns the current time.
     */
    virtual double time() = 0;

    /*!
     * \brief Returns the current delay in seconds.
     */
    virtual double delay() = 0;
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_TIME_DEPENDENT_DELAY_H */
