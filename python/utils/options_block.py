#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import argparse
import shlex


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
        if options is not None and type(options) is not str:
            self.options = options
            return

        p = argparse.ArgumentParser(prog=self.__class__.__name__)
        self.add_options(p)
        self.options = p.parse_args(shlex.split(options) if options else [])
