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

    def test_check_all_satyaml_files(self):
        for yml in satyaml.yamlfiles.yaml_files():
            with self.subTest(satyaml = yml):
                satyaml.yamlfiles.check_yaml(yml)

if __name__ == '__main__':
    gr_unittest.run(qa_satyaml)
