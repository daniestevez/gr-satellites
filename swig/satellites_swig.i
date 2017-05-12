/* -*- c++ -*- */

#define SATELLITES_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "satellites_swig_doc.i"

%{
#include "satellites/decode_rs.h"
#include "satellites/ao40_syncframe.h"
#include "satellites/ao40_deinterleaver.h"
#include "satellites/ao40_rs_decoder.h"
%}

%include "satellites/decode_rs.h"
GR_SWIG_BLOCK_MAGIC2(satellites, decode_rs);

%include "satellites/ao40_syncframe.h"
GR_SWIG_BLOCK_MAGIC2(satellites, ao40_syncframe);
%include "satellites/ao40_deinterleaver.h"
GR_SWIG_BLOCK_MAGIC2(satellites, ao40_deinterleaver);
%include "satellites/ao40_rs_decoder.h"
GR_SWIG_BLOCK_MAGIC2(satellites, ao40_rs_decoder);
