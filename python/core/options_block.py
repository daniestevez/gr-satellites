#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Daniel Estevez <daniel@destevez.net>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

import argparse

class options_block:
    """
    Class used to add default option parsing to blocks

    A block using this class should inherit both from a GNU
    Radio block class (gr.hier_block2, for example) and options_block.
    It should have a @classmethod add_options(cls, parser) that
    adds class specific options to an argparse parser.

    It should also have an options = None parameter in its __init__()
    method. The __init__() method should call options_block.__init__(options).
    Then options should be access as self.options.

    This class automatically set options to default values even if no options
    arguments was passed to the child class __init__() method.
    
    Args:
        options: options from argparse
    """
    def __init__(self, options):
        if options is not None:
            self.options = options
            return

        p = argparse.ArgumentParser()
        self.add_options(p)
        self.options = p.parse_args([])
