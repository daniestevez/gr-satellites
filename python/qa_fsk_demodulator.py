#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
from math import pi

from gnuradio import blocks, gr, gr_unittest
import numpy as np

try:
    import python as satellites
except ImportError:
    pass
else:
    import sys
    sys.modules['satellites'] = satellites

from satellites.components.demodulators import (
    afsk_demodulator, fsk_demodulator)


class qa_fsk_demodulator(gr_unittest.TestCase):
    def test_default_deviation(self):
        for baudrate, expected in ((1200, 3000), (11996, 3000),
                                   (12000, 3000), (12004, 3001),
                                   (38400, 9600)):
            with self.subTest(baudrate=baudrate):
                demod = fsk_demodulator(baudrate, 192000, True)
                self.assertAlmostEqual(
                    demod.demod.gain(), 192000 / (2 * pi * expected),
                    places=5)

    def test_explicit_deviation(self):
        parser = argparse.ArgumentParser()
        fsk_demodulator.add_options(parser)
        for deviation in (600, -600, 5000, -5000):
            for kwargs in ({'deviation': deviation},
                           {'options': f'--deviation {deviation}'},
                           {'options': parser.parse_args(
                               ['--deviation', str(deviation)])},
                           {'deviation': deviation,
                            'options': '--deviation 7000'}):
                with self.subTest(kwargs=kwargs):
                    demod = fsk_demodulator(38400, 192000, True, **kwargs)
                    self.assertAlmostEqual(
                        demod.demod.gain(),
                        192000 / (2 * pi * deviation), places=4)

    def test_afsk_deviation(self):
        demod = afsk_demodulator(
            1200, 48000, False, 1700, 500, options='--deviation 7000')
        self.assertAlmostEqual(demod.fsk.demod.gain(), 48000 / (2*pi*500), 5)

    def test_shared_options(self):
        parser = argparse.ArgumentParser()
        fsk_demodulator.add_options(parser)
        options = parser.parse_args([])
        low = fsk_demodulator(1200, 192000, True, options=options)
        high = fsk_demodulator(38400, 192000, True, options=options)
        self.assertAlmostEqual(low.demod.gain(), 192000 / (2*pi*3000), 5)
        self.assertAlmostEqual(high.demod.gain(), 192000 / (2*pi*9600), 5)
        self.assertIsNone(options.deviation)

    def test_iq_signal(self):
        for baudrate, deviation in ((1200, 3000), (38400, 9600)):
            with self.subTest(baudrate=baudrate):
                samp_rate = 192000
                samples = np.exp(
                    2j * pi * deviation / samp_rate * np.arange(50000))
                source = blocks.vector_source_c(samples.tolist())
                demod = fsk_demodulator(
                    baudrate, samp_rate, True, dc_block=False)
                sink = blocks.vector_sink_f()
                tb = gr.top_block()
                tb.connect(source, demod, sink)
                tb.run()
                output = np.array(sink.data())
                self.assertGreater(output.size, 100)
                np.testing.assert_allclose(output[-100:], 1, atol=0.02)

    def test_fsk_symbols(self):
        symbols = 2 * np.random.default_rng(42).integers(0, 2, 4096) - 1
        for baudrate, samp_rate, deviation in ((1200, 48000, 3000),
                                               (38400, 192000, 9600)):
            with self.subTest(baudrate=baudrate):
                phase = np.cumsum(np.repeat(symbols, samp_rate // baudrate))
                phase = phase * (2 * pi * deviation / samp_rate)
                source = blocks.vector_source_c(np.exp(1j * phase).tolist())
                demod = fsk_demodulator(baudrate, samp_rate, True)
                sink = blocks.vector_sink_f()
                tb = gr.top_block()
                tb.connect(source, demod, sink)
                tb.run()
                output = np.sign(np.array(sink.data())[500:-100])
                self.assertGreater(output.size, 3000)
                offset = np.argmax(np.correlate(symbols, output, mode='valid'))
                np.testing.assert_array_equal(
                    output, symbols[offset:offset + len(output)])

    def test_real_input_polarity(self):
        for options, expected in (('', 1), ('--deviation -600', -1)):
            with self.subTest(options=options):
                source = blocks.vector_source_f([1.0] * 20000)
                demod = fsk_demodulator(
                    9600, 48000, False, dc_block=False, options=options)
                sink = blocks.vector_sink_f()
                tb = gr.top_block()
                tb.connect(source, demod, sink)
                tb.run()
                output = np.array(sink.data())
                self.assertGreater(output.size, 100)
                np.testing.assert_allclose(output[-100:], expected, atol=0.02)


if __name__ == '__main__':
    gr_unittest.run(qa_fsk_demodulator)
