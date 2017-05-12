/* -*- c++ -*- */

#define SATELLITES_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "satellites_swig_doc.i"

%{
#include "satellites/decode_rs.h"
%}

%include "satellites/decode_rs.h"
GR_SWIG_BLOCK_MAGIC2(satellites, decode_rs);
