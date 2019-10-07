#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# This application is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This application is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# The presence of this file turns this directory into a Python package

'''
gr-satellites datasink components

The datasinks consume frames or packets in order to do something
useful with them (printing telemetry, reconstructing images,
storing to file, etc.)

The input to these blocks are PDUs with the frames.
'''

from ... import sat_1kuns_pf_image_decoder
from ... import sat_1kuns_pf_telemetry_parser
from ... import gomx3_beacon_parser

from .kiss_file_sink import kiss_file_sink
from .telemetry_submit import telemetry_submit
