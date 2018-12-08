/* -*- c++ -*- */

#define SATELLITES_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "satellites_swig_doc.i"

%{
#include "satellites/decode_rs.h"
#include "satellites/encode_rs.h"
#include "satellites/ao40_syncframe.h"
#include "satellites/ao40_deinterleaver.h"
#include "satellites/ao40_rs_decoder.h"
#include "satellites/ax100_decode.h"
#include "satellites/u482c_decode.h"
#include "satellites/lilacsat1_demux.h"
#include "satellites/varlen_packet_tagger.h"
#include "satellites/varlen_packet_framer.h"
#include "satellites/nusat_decoder.h"
#include "satellites/rscode_decoder.h"
#include "satellites/ao40_syncframe_soft.h"
#include "satellites/ao40_deinterleaver_soft.h"
#include "satellites/descrambler308.h"
#include "satellites/decode_rs_general.h"
%}

%include "satellites/decode_rs.h"
GR_SWIG_BLOCK_MAGIC2(satellites, decode_rs);
%include "satellites/encode_rs.h"
GR_SWIG_BLOCK_MAGIC2(satellites, encode_rs);
%include "satellites/ao40_syncframe.h"
GR_SWIG_BLOCK_MAGIC2(satellites, ao40_syncframe);
%include "satellites/ao40_deinterleaver.h"
GR_SWIG_BLOCK_MAGIC2(satellites, ao40_deinterleaver);
%include "satellites/ao40_rs_decoder.h"
GR_SWIG_BLOCK_MAGIC2(satellites, ao40_rs_decoder);
%include "satellites/ax100_decode.h"
GR_SWIG_BLOCK_MAGIC2(satellites, ax100_decode);
%include "satellites/u482c_decode.h"
GR_SWIG_BLOCK_MAGIC2(satellites, u482c_decode);
%include "satellites/lilacsat1_demux.h"
GR_SWIG_BLOCK_MAGIC2(satellites, lilacsat1_demux);
%include "satellites/varlen_packet_tagger.h"
GR_SWIG_BLOCK_MAGIC2(satellites, varlen_packet_tagger);
%include "satellites/varlen_packet_framer.h"
GR_SWIG_BLOCK_MAGIC2(satellites, varlen_packet_framer);
%include "satellites/nusat_decoder.h"
GR_SWIG_BLOCK_MAGIC2(satellites, nusat_decoder);
%include "satellites/rscode_decoder.h"
GR_SWIG_BLOCK_MAGIC2(satellites, rscode_decoder);
%include "satellites/ao40_syncframe_soft.h"
GR_SWIG_BLOCK_MAGIC2(satellites, ao40_syncframe_soft);
%include "satellites/ao40_deinterleaver_soft.h"
GR_SWIG_BLOCK_MAGIC2(satellites, ao40_deinterleaver_soft);
%include "satellites/descrambler308.h"
GR_SWIG_BLOCK_MAGIC2(satellites, descrambler308);
%include "satellites/decode_rs_general.h"
GR_SWIG_BLOCK_MAGIC2(satellites, decode_rs_general);
