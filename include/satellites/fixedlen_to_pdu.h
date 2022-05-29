/* -*- c++ -*- */
/*
 * Copyright 2022 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_FIXEDLEN_TO_PDU_H
#define INCLUDED_SATELLITES_FIXEDLEN_TO_PDU_H

#include <gnuradio/blocks/pdu.h>
#include <gnuradio/sync_block.h>
#include <satellites/api.h>

namespace gr {
namespace satellites {

/*!
 * \brief Fixedlen to PDU
 * \ingroup satellites
 *
 */
class SATELLITES_API fixedlen_to_pdu : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<fixedlen_to_pdu> sptr;

    /*!
     * Make a Fixedlen to PDU block.
     */
    static sptr make(blocks::pdu::vector_type type,
                     const std::string& syncword_tag,
                     size_t packet_len,
                     bool pack = false);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_FIXEDLEN_TO_PDU_H */
