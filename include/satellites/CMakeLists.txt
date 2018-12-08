# Copyright 2011,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Install public header files
########################################################################
install(FILES
    api.h
    decode_rs.h
    encode_rs.h
    ao40_syncframe.h
    ao40_deinterleaver.h
    ao40_rs_decoder.h
    ax100_decode.h
    u482c_decode.h
    lilacsat1_demux.h
    varlen_packet_tagger.h
    varlen_packet_framer.h
    nusat_decoder.h
    rscode_decoder.h
    ao40_syncframe_soft.h
    ao40_deinterleaver_soft.h
    descrambler308.h
    decode_rs_general.h
    DESTINATION include/satellites
)
