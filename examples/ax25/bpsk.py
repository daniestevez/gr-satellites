#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BPSK example
# Author: Daniel Estevez
# Description: This example implements an FSK 9k6 AX.25 G3RUH transceiver
# GNU Radio version: v3.11.0.0git-75-g67e88516

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import network
import satellites



from gnuradio import qtgui

class bpsk(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "BPSK example", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("BPSK example")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "bpsk")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_calcdist([-1, 1], [0, 1],
        2, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.variable_adaptive_algorithm_1 = variable_adaptive_algorithm_1 = digital.adaptive_algorithm_lms( variable_constellation_0, .0001).base()
        self.samp_rate = samp_rate = 9600
        self.samp_per_sym = samp_per_sym = 8

        ##################################################
        # Blocks
        ##################################################
        self.satellites_pdu_to_kiss_0 = satellites.pdu_to_kiss(control_byte = True, include_timestamp = False)
        self.satellites_nrzi_encode_0 = satellites.nrzi_encode()
        self.satellites_nrzi_decode_0 = satellites.nrzi_decode()
        self.satellites_kiss_to_pdu_0 = satellites.kiss_to_pdu(True)
        self.satellites_hdlc_framer_0 = satellites.hdlc_framer(preamble_bytes=50, postamble_bytes=7)
        self.satellites_hdlc_deframer_0 = satellites.hdlc_deframer(check_fcs=True, max_length=10000)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            200, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.pdu_pdu_to_tagged_stream_1 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.network_socket_pdu_0 = network.socket_pdu('TCP_SERVER', '', '52001', 10000, True)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            5,
            firdes.low_pass(
                1,
                48000,
                1500,
                500,
                window.WIN_HAMMING,
                6.76))
        self.hilbert_fc_0 = filter.hilbert_fc(65, window.WIN_HAMMING, 6.76)
        self.digital_psk_mod_0 = digital.psk.psk_mod(
            constellation_points=2,
            mod_code="none",
            differential=False,
            samples_per_symbol=samp_per_sym*5,
            excess_bw=0.35,
            verbose=False,
            log=False)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(samp_per_sym, 0.05, firdes.root_raised_cosine(16, 16, 1.0/float(samp_per_sym), 0.35, 11*samp_per_sym*16), 16, 8, 0.05, 2)
        self.digital_linear_equalizer_0 = digital.linear_equalizer(2, 2, variable_adaptive_algorithm_1, True, [ ], 'corr_est')
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(samp_per_sym, 0.350, 100, 0.010)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc(0.02, 2, False)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.5)
        self.blocks_message_debug_0 = blocks.message_debug(True)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.audio_source_0 = audio.source(48000, '', True)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(48000, analog.GR_COS_WAVE, 1500, 0.5, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(48000, analog.GR_COS_WAVE, -1500, 1, 0, 0)
        self.analog_feedforward_agc_cc_0 = analog.feedforward_agc_cc(1024, 2)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.network_socket_pdu_0, 'pdus'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.satellites_hdlc_deframer_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.satellites_hdlc_deframer_0, 'out'), (self.satellites_pdu_to_kiss_0, 'in'))
        self.msg_connect((self.satellites_hdlc_framer_0, 'out'), (self.pdu_pdu_to_tagged_stream_1, 'pdus'))
        self.msg_connect((self.satellites_kiss_to_pdu_0, 'out'), (self.satellites_hdlc_framer_0, 'in'))
        self.msg_connect((self.satellites_pdu_to_kiss_0, 'out'), (self.network_socket_pdu_0, 'pdus'))
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.audio_source_0, 0), (self.hilbert_fc_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.digital_psk_mod_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.satellites_nrzi_decode_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.digital_linear_equalizer_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.digital_linear_equalizer_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_linear_equalizer_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0_0, 0))
        self.connect((self.digital_psk_mod_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.hilbert_fc_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_feedforward_agc_cc_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.satellites_kiss_to_pdu_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_1, 0), (self.satellites_nrzi_encode_0, 0))
        self.connect((self.satellites_nrzi_decode_0, 0), (self.satellites_hdlc_deframer_0, 0))
        self.connect((self.satellites_nrzi_encode_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "bpsk")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_constellation_0(self):
        return self.variable_constellation_0

    def set_variable_constellation_0(self, variable_constellation_0):
        self.variable_constellation_0 = variable_constellation_0

    def get_variable_adaptive_algorithm_1(self):
        return self.variable_adaptive_algorithm_1

    def set_variable_adaptive_algorithm_1(self, variable_adaptive_algorithm_1):
        self.variable_adaptive_algorithm_1 = variable_adaptive_algorithm_1

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.digital_pfb_clock_sync_xxx_0.update_taps(firdes.root_raised_cosine(16, 16, 1.0/float(self.samp_per_sym), 0.35, 11*self.samp_per_sym*16))




def main(top_block_cls=bpsk, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
