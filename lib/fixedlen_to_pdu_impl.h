/* -*- c++ -*- */
/*
 * Copyright 2022 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_FIXEDLEN_TO_PDU_IMPL_H
#define INCLUDED_SATELLITES_FIXEDLEN_TO_PDU_IMPL_H

#include <gnuradio/blocks/pdu.h>
#include <satellites/fixedlen_to_pdu.h>
#include <vector>

namespace gr {
namespace satellites {

class fixedlen_to_pdu_impl : public fixedlen_to_pdu
{
private:
    const blocks::pdu::vector_type d_type;
    const bool d_pack;
    const size_t d_packetlen;
    const size_t d_packet_nbytes;
    const size_t d_pdu_items;
    const pmt::pmt_t d_syncword_tag;
    std::vector<uint8_t> d_history;
    size_t d_write_ptr_item;
    size_t d_write_ptr_byte;
    std::vector<uint8_t> d_packet;
    std::vector<tag_t> d_tags_in_window;
    std::list<uint64_t> d_tag_offsets;

    void pack_packet();
    void update_history(const uint8_t* in, int noutput_items);

public:
    fixedlen_to_pdu_impl(blocks::pdu::vector_type type,
                         const std::string& syncword_tag,
                         size_t packet_len,
                         bool pack);
    ~fixedlen_to_pdu_impl();

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_FIXEDLEN_TO_PDU_IMPL_H */
