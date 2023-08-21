/* -*- c++ -*- */
/*
 * Copyright 2019 Free Software Foundation, Inc.
 * Copyright 2023 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * This is a copy of the GNU Radio Selector block modified to consume all the
 * items that are available on inactive inputs. This is required to use selector
 * blocks to bypass sections of the flowgraph. See
 * https://github.com/gnuradio/gnuradio/issues/6792
 * for more information.
 *
 */

#ifndef INCLUDED_SATELLITES_SELECTOR_H
#define INCLUDED_SATELLITES_SELECTOR_H

#include <gnuradio/block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief output[output_index][i] = input[input_index][i]
 * \ingroup satellites
 *
 * \details
 * Connect the sink at input index to the source at output index.
 *
 * All the samples available from other input ports are consumed and dumped.
 *
 * Other output ports produce no samples.
 *
 */
class SATELLITES_API selector : virtual public gr::block
{
public:
    typedef boost::shared_ptr<selector> sptr;

    /*!
     * Create new selector block and return a shared pointer to it
     *
     * \param itemsize size of the input and output items
     * \param input_index the initially active input index
     * \param output_index the initially active output index
     */
    static sptr
    make(size_t itemsize, unsigned int input_index, unsigned int output_index);

    /*!
     * When enabled is set to false, no output samples are produced.
     * Otherwise samples are copied to the selected output port
     */
    virtual void set_enabled(bool enable) = 0;
    virtual bool enabled() const = 0;

    virtual void set_input_index(unsigned int input_index) = 0;
    virtual int input_index() const = 0;

    virtual void set_output_index(unsigned int output_index) = 0;
    virtual int output_index() const = 0;
};

} /* namespace satellites */
} /* namespace gr */

#endif /* INCLUDED_SATELLITES_SELECTOR_H */
