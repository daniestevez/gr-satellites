#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr_unittest
import satyaml

class qa_satyaml(gr_unittest.TestCase):

    def test_001_t(self):
        satyaml.yamlfiles.check_all_yaml()

if __name__ == '__main__':
    gr_unittest.run(qa_satyaml)
