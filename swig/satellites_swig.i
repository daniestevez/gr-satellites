/* -*- c++ -*- */

#define SATELLITES_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "satellites_swig_doc.i"

%{
#include "satellites/ax100_decode.h"
#include "satellites/convolutional_encoder.h"
#include "satellites/decode_ra_code.h"
#include "satellites/decode_rs.h"
#include "satellites/descrambler308.h"
#include "satellites/distributed_syncframe_soft.h"
#include "satellites/encode_rs.h"
#include "satellites/lilacsat1_demux.h"
#include "satellites/matrix_deinterleaver_soft.h"
#include "satellites/nrzi_decode.h"
#include "satellites/nrzi_encode.h"
#include "satellites/nusat_decoder.h"
#include "satellites/pdu_add_meta.h"
#include "satellites/pdu_head_tail.h"
#include "satellites/pdu_length_filter.h"
#include "satellites/u482c_decode.h"
#include "satellites/varlen_packet_framer.h"
#include "satellites/varlen_packet_tagger.h"
#include "satellites/viterbi_decoder.h"
%}

%include "satellites/ax100_decode.h"
GR_SWIG_BLOCK_MAGIC2(satellites, ax100_decode);
%include "satellites/convolutional_encoder.h"
GR_SWIG_BLOCK_MAGIC2(satellites, convolutional_encoder);
%include "satellites/decode_ra_code.h"
GR_SWIG_BLOCK_MAGIC2(satellites, decode_ra_code);
%include "satellites/decode_rs.h"
GR_SWIG_BLOCK_MAGIC2(satellites, decode_rs);
%include "satellites/descrambler308.h"
GR_SWIG_BLOCK_MAGIC2(satellites, descrambler308);
%include "satellites/distributed_syncframe_soft.h"
GR_SWIG_BLOCK_MAGIC2(satellites, distributed_syncframe_soft);
%include "satellites/encode_rs.h"
GR_SWIG_BLOCK_MAGIC2(satellites, encode_rs);
%include "satellites/lilacsat1_demux.h"
GR_SWIG_BLOCK_MAGIC2(satellites, lilacsat1_demux);
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
%include "satellites/u482c_decode.h"
GR_SWIG_BLOCK_MAGIC2(satellites, u482c_decode);
%include "satellites/varlen_packet_framer.h"
GR_SWIG_BLOCK_MAGIC2(satellites, varlen_packet_framer);
%include "satellites/varlen_packet_tagger.h"
GR_SWIG_BLOCK_MAGIC2(satellites, varlen_packet_tagger);
%include "satellites/viterbi_decoder.h"
GR_SWIG_BLOCK_MAGIC2(satellites, viterbi_decoder);

