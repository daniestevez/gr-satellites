
/*
 * This file was automatically generated using swig_doc.py.
 *
 * Any changes to it will be lost next time it is regenerated.
 */




%feature("docstring") gr::satellites::ao40_deinterleaver "<+description of block+>"

%feature("docstring") gr::satellites::ao40_deinterleaver::make "Return a shared_ptr to a new instance of satellites::ao40_deinterleaver.

To avoid accidental use of raw pointers, satellites::ao40_deinterleaver's constructor is in a private implementation class. satellites::ao40_deinterleaver::make is the public interface for creating new instances.

Params: (NONE)"

%feature("docstring") gr::satellites::ao40_deinterleaver_soft "<+description of block+>"

%feature("docstring") gr::satellites::ao40_deinterleaver_soft::make "Return a shared_ptr to a new instance of satellites::ao40_deinterleaver_soft.

To avoid accidental use of raw pointers, satellites::ao40_deinterleaver_soft's constructor is in a private implementation class. satellites::ao40_deinterleaver_soft::make is the public interface for creating new instances.

Params: (NONE)"

%feature("docstring") gr::satellites::ao40_rs_decoder "<+description of block+>"

%feature("docstring") gr::satellites::ao40_rs_decoder::make "Return a shared_ptr to a new instance of satellites::ao40_rs_decoder.

To avoid accidental use of raw pointers, satellites::ao40_rs_decoder's constructor is in a private implementation class. satellites::ao40_rs_decoder::make is the public interface for creating new instances.

Params: (verbose)"

%feature("docstring") gr::satellites::ao40_syncframe "<+description of block+>"

%feature("docstring") gr::satellites::ao40_syncframe::make "Return a shared_ptr to a new instance of ao40::syncframe.

To avoid accidental use of raw pointers, ao40::syncframe's constructor is in a private implementation class. ao40::syncframe::make is the public interface for creating new instances.

Params: (threshold)"

%feature("docstring") gr::satellites::ao40_syncframe_soft "<+description of block+>"

%feature("docstring") gr::satellites::ao40_syncframe_soft::make "Return a shared_ptr to a new instance of satellites::syncframe_soft.

To avoid accidental use of raw pointers, satellites::syncframe_soft's constructor is in a private implementation class. satellites::syncframe_soft::make is the public interface for creating new instances.

Params: (threshold)"

%feature("docstring") gr::satellites::ax100_decode "<+description of block+>"

%feature("docstring") gr::satellites::ax100_decode::make "Return a shared_ptr to a new instance of satellites::ax100_decode.

To avoid accidental use of raw pointers, satellites::ax100_decode's constructor is in a private implementation class. satellites::ax100_decode::make is the public interface for creating new instances.

Params: (verbose)"

%feature("docstring") gr::satellites::decode_rs "<+description of block+>"

%feature("docstring") gr::satellites::decode_rs::make "Return a shared_ptr to a new instance of satellites::decode_rs.

To avoid accidental use of raw pointers, satellites::decode_rs's constructor is in a private implementation class. satellites::decode_rs::make is the public interface for creating new instances.

Params: (verbose, basis)"

%feature("docstring") gr::satellites::decode_rs_general "<+description of block+>"

%feature("docstring") gr::satellites::decode_rs_general::make "Return a shared_ptr to a new instance of satellites::decode_rs_general.

To avoid accidental use of raw pointers, satellites::decode_rs_general's constructor is in a private implementation class. satellites::decode_rs_general::make is the public interface for creating new instances.

Params: (gfpoly, fcr, prim, nroots, verbose)"

%feature("docstring") gr::satellites::decode_rs_interleaved "<+description of block+>"

%feature("docstring") gr::satellites::decode_rs_interleaved::make "Return a shared_ptr to a new instance of satellites::decode_rs_interleaved.

To avoid accidental use of raw pointers, satellites::decode_rs_interleaved's constructor is in a private implementation class. satellites::decode_rs_interleaved::make is the public interface for creating new instances.

Params: (verbose, basis, codewords)"

%feature("docstring") gr::satellites::descrambler308 "<+description of block+>"

%feature("docstring") gr::satellites::descrambler308::make "Return a shared_ptr to a new instance of satellites::descrambler308.

To avoid accidental use of raw pointers, satellites::descrambler308's constructor is in a private implementation class. satellites::descrambler308::make is the public interface for creating new instances.

Params: (NONE)"

%feature("docstring") gr::satellites::encode_rs "<+description of block+>"

%feature("docstring") gr::satellites::encode_rs::make "Return a shared_ptr to a new instance of satellites::encode_rs.

To avoid accidental use of raw pointers, satellites::encode_rs's constructor is in a private implementation class. satellites::encode_rs::make is the public interface for creating new instances.

Params: (basis)"

%feature("docstring") gr::satellites::lilacsat1_demux "<+description of block+>"

%feature("docstring") gr::satellites::lilacsat1_demux::make "Return a shared_ptr to a new instance of satellites::lilacsat1_demux.

To avoid accidental use of raw pointers, satellits::lilacsat1_demux's constructor is in a private implementation class. satellites::lilacsat1_demux::make is the public interface for creating new instances.

Params: (tag)"

%feature("docstring") gr::satellites::nusat_decoder "<+description of block+>"

%feature("docstring") gr::satellites::nusat_decoder::make "Return a shared_ptr to a new instance of satellites::nusat_decoder.

To avoid accidental use of raw pointers, satellites::nusat_decoder's constructor is in a private implementation class. satellites::nusat_decoder::make is the public interface for creating new instances.

Params: (NONE)"

%feature("docstring") gr::satellites::rscode_decoder "<+description of block+>"

%feature("docstring") gr::satellites::rscode_decoder::make "Return a shared_ptr to a new instance of satellites::rscode_decoder.

To avoid accidental use of raw pointers, satellites::rscode_decoder's constructor is in a private implementation class. satellites::rscode_decoder::make is the public interface for creating new instances.

Params: (npar)"

%feature("docstring") gr::satellites::u482c_decode "<+description of block+>"

%feature("docstring") gr::satellites::u482c_decode::make "Return a shared_ptr to a new instance of satellites::u482c_decode.

To avoid accidental use of raw pointers, satellites::u482c_decode's constructor is in a private implementation class. satellites::u482c_decode::make is the public interface for creating new instances.

Params: (verbose, viterbi, scrambler, rs)"

%feature("docstring") gr::satellites::varlen_packet_framer "insert a packet length field into a tagged stream

input: stream of bits (unpacked bytes) with packet_len tags output: a tagged stream of bits containing field length + packet bits

This block prepends a packet length field into a tagged stream."

%feature("docstring") gr::satellites::varlen_packet_framer::make "

Params: (packet_key, length_field_size, endianness, use_golay, sync_word)"

%feature("docstring") gr::satellites::varlen_packet_tagger "Examine input stream for sync tags and extract packet length.

input: stream of bits (unpacked bytes) with sync tags output: a tagged stream of bits containing just the received packets

This block uses the sync tag on the input stream to identify the header of packets. The length of each packet is extracted from the stream's header. The length of the header field and the endianness are parameters."

%feature("docstring") gr::satellites::varlen_packet_tagger::make "

Params: (sync_key, packet_key, length_field_size, max_packet_size, endianness, use_golay)"