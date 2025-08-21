/* -*- c++ -*- */
/*
 * Copyright 2022,2025 Daniel Estevez <daniel@destevez.net>
 *
 * This file is part of gr-satellites
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_SATELLITES_FIXEDLEN_TO_PDU_IMPL_H
#define INCLUDED_SATELLITES_FIXEDLEN_TO_PDU_IMPL_H

#include <satellites/fixedlen_to_pdu.h>
#include <optional>
#include <vector>

namespace gr {
namespace satellites {

struct packet_info {
    uint64_t offset;
    int length;
};

class fixedlen_to_pdu_impl : public fixedlen_to_pdu
{
private:
    const types::vector_type d_type;
    const size_t d_itemsize;
    const bool d_pack;
    const size_t d_packetlen;
    const pmt::pmt_t d_syncword_tag;
    const std::optional<pmt::pmt_t> d_packet_length_tag;
    std::vector<uint8_t> d_history;
    size_t d_write_ptr_item{ 0 };
    size_t d_write_ptr_byte{ 0 };
    std::vector<uint8_t> d_packet;
    std::vector<packet_info> d_packet_infos;
    std::vector<packet_info> d_new_packet_infos;

    void pack_packet(size_t size_bytes);
    void update_history(const uint8_t* in, int noutput_items);

public:
    fixedlen_to_pdu_impl(types::vector_type type,
                         const std::string& syncword_tag,
                         size_t packet_len,
                         bool pack,
                         const std::string& packet_len_tag_key);
    ~fixedlen_to_pdu_impl() override;

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items) override;
};

} // namespace satellites
} // namespace gr

#endif /* INCLUDED_SATELLITES_FIXEDLEN_TO_PDU_IMPL_H */
