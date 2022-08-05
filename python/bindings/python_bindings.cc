/*
 * Copyright 2020 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#include <pybind11/pybind11.h>

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

namespace py = pybind11;

// Headers for binding functions
/**************************************/
// The following comment block is used for
// gr_modtool to insert function prototypes
// Please do not delete
/**************************************/
// BINDING_FUNCTION_PROTOTYPES(
void bind_ax100_decode(py::module& m);
void bind_crc(py::module& m);
void bind_crc_append(py::module& m);
void bind_crc_check(py::module& m);
void bind_convolutional_encoder(py::module& m);
void bind_costas_loop_8apsk_cc(py::module& m);
void bind_decode_ra_code(py::module& m);
void bind_decode_rs(py::module& m);
void bind_descrambler308(py::module& m);
void bind_distributed_syncframe_soft(py::module& m);
void bind_doppler_correction(py::module& m);
void bind_encode_rs(py::module& m);
void bind_fixedlen_to_pdu(py::module& m);
void bind_lilacsat1_demux(py::module& m);
void bind_matrix_deinterleaver_soft(py::module& m);
void bind_nrzi_decode(py::module& m);
void bind_nrzi_encode(py::module& m);
void bind_nusat_decoder(py::module& m);
void bind_pdu_add_meta(py::module& m);
void bind_pdu_head_tail(py::module& m);
void bind_pdu_length_filter(py::module& m);
void bind_pdu_scrambler(py::module& m);
void bind_phase_unwrap(py::module& m);
void bind_u482c_decode(py::module& m);
void bind_varlen_packet_framer(py::module& m);
void bind_varlen_packet_tagger(py::module& m);
void bind_viterbi_decoder(py::module& m);
// ) END BINDING_FUNCTION_PROTOTYPES


// We need this hack because import_array() returns NULL
// for newer Python versions.
// This function is also necessary because it ensures access to the C API
// and removes a warning.
void* init_numpy()
{
    import_array();
    return NULL;
}

PYBIND11_MODULE(satellites_python, m)
{
    // Initialize the numpy C API
    // (otherwise we will see segmentation faults)
    init_numpy();

    // Allow access to base block methods
    py::module::import("gnuradio.gr");

    /**************************************/
    // The following comment block is used for
    // gr_modtool to insert binding function calls
    // Please do not delete
    /**************************************/
    // BINDING_FUNCTION_CALLS(
    bind_ax100_decode(m);
    bind_crc(m);
    bind_crc_append(m);
    bind_crc_check(m);
    bind_convolutional_encoder(m);
    bind_costas_loop_8apsk_cc(m);
    bind_decode_ra_code(m);
    bind_decode_rs(m);
    bind_descrambler308(m);
    bind_distributed_syncframe_soft(m);
    bind_doppler_correction(m);
    bind_encode_rs(m);
    bind_fixedlen_to_pdu(m);
    bind_lilacsat1_demux(m);
    bind_matrix_deinterleaver_soft(m);
    bind_nrzi_decode(m);
    bind_nrzi_encode(m);
    bind_nusat_decoder(m);
    bind_pdu_add_meta(m);
    bind_pdu_head_tail(m);
    bind_pdu_length_filter(m);
    bind_pdu_scrambler(m);
    bind_phase_unwrap(m);
    bind_u482c_decode(m);
    bind_varlen_packet_framer(m);
    bind_varlen_packet_tagger(m);
    bind_viterbi_decoder(m);
    // ) END BINDING_FUNCTION_CALLS
}
