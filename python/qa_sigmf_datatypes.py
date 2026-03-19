#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 gr-satellites contributors
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import json
import os
import tempfile

import numpy as np
from gnuradio import gr_unittest

# (name, numpy_dtype, sizeof_bytes, already_complex, is_real)
# To add a datatype: append a row and add the elif branch + datatypes_supported
# entry in apps/gr_satellites.
DATATYPES = [
    ('ci16_le',   np.int16,      2,   False,  False),
    ('cf32_le',   np.complex64,  8,   True,   False),
    ('ci8',       np.int8,       1,   False,  False),
    ('rf32_le',   np.float32,    4,   False,  True),
    ('ri16_le',   np.int16,      2,   False,  True),
]

APPS_GR_SATELLITES = os.path.join(
    os.path.dirname(__file__), '..', 'apps', 'gr_satellites')


class qa_sigmf_datatypes(gr_unittest.TestCase):

    def _make_sigmf_pair(self, datatype, samples, samp_rate=48000):
        d = tempfile.mkdtemp()
        data_path = os.path.join(d, 'test.sigmf-data')
        meta_path = os.path.join(d, 'test.sigmf-meta')
        samples.tofile(data_path)
        meta = {
            'global': {
                'core:datatype': datatype,
                'core:sample_rate': samp_rate,
            },
            'captures': [{'core:sample_start': 0}],
            'annotations': [],
        }
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f)
        return data_path, meta_path

    def _test_datatype(self, name, numpy_dtype, sizeof_bytes, already_complex,
                       is_real=False):
        n = 16
        if already_complex:
            original = (np.arange(n) + 1j * np.arange(n, 2 * n)).astype(numpy_dtype)
        elif is_real:
            original = np.arange(n, dtype=numpy_dtype)
        else:
            original = np.arange(2 * n, dtype=numpy_dtype)

        data_path, _ = self._make_sigmf_pair(name, original)

        file_size = os.path.getsize(data_path)
        self.assertEqual(
            file_size % sizeof_bytes, 0,
            f'{name}: file size {file_size} not a multiple of sizeof={sizeof_bytes}')

        recovered = np.fromfile(data_path, dtype=numpy_dtype)
        np.testing.assert_array_equal(
            recovered, original,
            err_msg=f'{name}: numpy round-trip mismatch')

        expected_samples = file_size // sizeof_bytes
        self.assertEqual(
            len(recovered), expected_samples,
            f'{name}: sample count mismatch '
            f'(expected {expected_samples}, got {len(recovered)})')

    def test_all_datatypes(self):
        """sizeof, endianness, and sample-count checks for every datatype."""
        for (name, dtype, sizeof_bytes, already_complex, is_real) in DATATYPES:
            with self.subTest(datatype=name):
                self._test_datatype(name, dtype, sizeof_bytes, already_complex,
                                    is_real)

    def test_datatypes_supported_list_is_complete(self):
        """Every DATATYPES entry must appear in datatypes_supported in apps/gr_satellites."""
        with open(APPS_GR_SATELLITES, encoding='utf-8') as f:
            source = f.read()
        for (name, *_) in DATATYPES:
            self.assertIn(
                f"'{name}'", source,
                f"'{name}' missing from datatypes_supported in apps/gr_satellites")

    def test_elif_branch_exists_for_each_datatype(self):
        """Every DATATYPES entry must have a dispatch branch in setup_sigmf_input()."""
        with open(APPS_GR_SATELLITES, encoding='utf-8') as f:
            source = f.read()
        for (name, *_) in DATATYPES:
            self.assertIn(
                f"== '{name}'", source,
                f"No dispatch branch found for datatype '{name}' "
                f"in apps/gr_satellites")


if __name__ == '__main__':
    gr_unittest.run(qa_sigmf_datatypes)
