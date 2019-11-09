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
gr-satellites telemetry definitions

These are telemetry defintions. Most of them are just a construct
object, but in more complex cases, another class supporting the
.parse method and relying on construct is used.
'''

from .ax25 import ax25
from .gomx_3 import gomx_3
from .sat_1kuns_pf import sat_1kuns_pf
from .sat_3cat_1 import sat_3cat_1
