/* -*- c++ -*- */

#define SATELLITES_API
#define BLOCKS_API

%include "gnuradio.i"           // the common stuff
%include "gnuradio/blocks/pdu.h"

//load generated python docstrings
%include "satellites_swig_doc.i"

%{
#include "satellites/ax100_decode.h"
#include "satellites/convolutional_encoder.h"
#include "satellites/costas_loop_8apsk_cc.h"
#include "satellites/crc.h"
#include "satellites/crc_append.h"
#include "satellites/crc_check.h"
#include "satellites/decode_ra_code.h"
#include "satellites/decode_rs.h"
#include "satellites/descrambler308.h"
#include "satellites/distributed_syncframe_soft.h"
#include "satellites/doppler_correction.h"
#include "satellites/encode_rs.h"
#include "satellites/fixedlen_to_pdu.h"
#include "satellites/frame_counter.h"
#include "satellites/lilacsat1_demux.h"
#include "satellites/manchester_sync.h"
#include "satellites/matrix_deinterleaver_soft.h"
#include "satellites/nrzi_decode.h"
#include "satellites/nrzi_encode.h"
#include "satellites/nusat_decoder.h"
#include "satellites/pdu_add_meta.h"
#include "satellites/pdu_head_tail.h"
#include "satellites/pdu_length_filter.h"
#include "satellites/pdu_scrambler.h"
#include "satellites/phase_unwrap.h"
#include "satellites/selector.h"
#include "satellites/time_dependent_delay.h"
#include "satellites/u482c_decode.h"
#include "satellites/u482c_encode.h"
#include "satellites/varlen_packet_framer.h"
#include "satellites/varlen_packet_tagger.h"
#include "satellites/viterbi_decoder.h"
%}

%include "satellites/ax100_decode.h"
GR_SWIG_BLOCK_MAGIC2(satellites, ax100_decode);
%include "satellites/costas_loop_8apsk_cc.h"
GR_SWIG_BLOCK_MAGIC2(satellites, costas_loop_8apsk_cc);
%include "satellites/convolutional_encoder.h"
GR_SWIG_BLOCK_MAGIC2(satellites, convolutional_encoder);
%include "satellites/crc.h"
%include "satellites/crc_append.h"
GR_SWIG_BLOCK_MAGIC2(satellites, crc_append);
%include "satellites/crc_check.h"
GR_SWIG_BLOCK_MAGIC2(satellites, crc_check);
%include "satellites/decode_ra_code.h"
GR_SWIG_BLOCK_MAGIC2(satellites, decode_ra_code);
%include "satellites/decode_rs.h"
GR_SWIG_BLOCK_MAGIC2(satellites, decode_rs);
%include "satellites/descrambler308.h"
GR_SWIG_BLOCK_MAGIC2(satellites, descrambler308);
%include "satellites/distributed_syncframe_soft.h"
GR_SWIG_BLOCK_MAGIC2(satellites, distributed_syncframe_soft);
%include "satellites/doppler_correction.h"
GR_SWIG_BLOCK_MAGIC2(satellites, doppler_correction);
%include "satellites/encode_rs.h"
GR_SWIG_BLOCK_MAGIC2(satellites, encode_rs);
%include "satellites/fixedlen_to_pdu.h"
GR_SWIG_BLOCK_MAGIC2(satellites, fixedlen_to_pdu);
%include "satellites/frame_counter.h"
GR_SWIG_BLOCK_MAGIC2(satellites, frame_counter);
%include "satellites/lilacsat1_demux.h"
GR_SWIG_BLOCK_MAGIC2(satellites, lilacsat1_demux);
%include "satellites/manchester_sync.h"
GR_SWIG_BLOCK_MAGIC2_TMPL(satellites, manchester_sync_cc, manchester_sync<gr_complex>);
GR_SWIG_BLOCK_MAGIC2_TMPL(satellites, manchester_sync_ff, manchester_sync<float>);
%include "satellites/matrix_deinterleaver_soft.h"
GR_SWIG_BLOCK_MAGIC2(satellites, matrix_deinterleaver_soft);
%include "satellites/nrzi_decode.h"
GR_SWIG_BLOCK_MAGIC2(satellites, nrzi_decode);
%include "satellites/nrzi_encode.h"
GR_SWIG_BLOCK_MAGIC2(satellites, nrzi_encode);
%include "satellites/nusat_decoder.h"
GR_SWIG_BLOCK_MAGIC2(satellites, nusat_decoder);
%include "satellites/pdu_add_meta.h"
GR_SWIG_BLOCK_MAGIC2(satellites, pdu_add_meta);
%include "satellites/pdu_head_tail.h"
GR_SWIG_BLOCK_MAGIC2(satellites, pdu_head_tail);
%include "satellites/pdu_length_filter.h"
GR_SWIG_BLOCK_MAGIC2(satellites, pdu_length_filter);
%include "satellites/pdu_scrambler.h"
GR_SWIG_BLOCK_MAGIC2(satellites, pdu_scrambler);
%include "satellites/phase_unwrap.h"
GR_SWIG_BLOCK_MAGIC2(satellites, phase_unwrap);
%include "satellites/selector.h"
GR_SWIG_BLOCK_MAGIC2(satellites, selector);
%include "satellites/time_dependent_delay.h"
GR_SWIG_BLOCK_MAGIC2(satellites, time_dependent_delay);
%include "satellites/u482c_decode.h"
GR_SWIG_BLOCK_MAGIC2(satellites, u482c_decode);
%include "satellites/u482c_encode.h"
GR_SWIG_BLOCK_MAGIC2(satellites, u482c_encode);
%include "satellites/varlen_packet_framer.h"
GR_SWIG_BLOCK_MAGIC2(satellites, varlen_packet_framer);
%include "satellites/varlen_packet_tagger.h"
GR_SWIG_BLOCK_MAGIC2(satellites, varlen_packet_tagger);
%include "satellites/viterbi_decoder.h"
GR_SWIG_BLOCK_MAGIC2(satellites, viterbi_decoder);

