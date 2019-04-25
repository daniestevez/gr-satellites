#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: MYSAT 1 decoder
# Author: Daniel Estevez
# Description: Decodes 1k2/9k6 BPSK + G3RUH telemetry from MYSAT 1
# Generated: Thu Apr 25 12:01:35 2019
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
from rms_agc import rms_agc  # grc-generated hier_block
import satellites
import sip
from gnuradio import qtgui


class mysat1(gr.top_block, Qt.QWidget):

    def __init__(self, bfo=1.5e3, callsign='', ip='::', latitude=0, longitude=0, port=7355, recstart=''):
        gr.top_block.__init__(self, "MYSAT 1 decoder")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("MYSAT 1 decoder")
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

        self.settings = Qt.QSettings("GNU Radio", "mysat1")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Parameters
        ##################################################
        self.bfo = bfo
        self.callsign = callsign
        self.ip = ip
        self.latitude = latitude
        self.longitude = longitude
        self.port = port
        self.recstart = recstart

        ##################################################
        # Variables
        ##################################################
        self.samp_per_sym = samp_per_sym = 8
        self.nfilts = nfilts = 16

        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 2, 1).base()

        self.samp_rate = samp_rate = 48000
        self.rrc_taps_9k6 = rrc_taps_9k6 = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(5), 0.35, 11*5*nfilts)
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(samp_per_sym), 0.35, 11*samp_per_sym*nfilts)

        ##################################################
        # Blocks
        ##################################################
        self.satellites_submit_0 = satellites.submit('https://db.satnogs.org/api/telemetry/', 44045, callsign, longitude, latitude, recstart)
        self.satellites_print_timestamp_0 = satellites.print_timestamp('%Y-%m-%d %H:%M:%S', True)
        self.satellites_pdu_to_kiss_0 = satellites.pdu_to_kiss()
        self.satellites_nrzi_decode_0_0 = satellites.nrzi_decode()
        self.satellites_nrzi_decode_0 = satellites.nrzi_decode()
        self.satellites_hdlc_deframer_0_0 = satellites.hdlc_deframer(check_fcs=False, max_length=10000)
        self.satellites_hdlc_deframer_0 = satellites.hdlc_deframer(check_fcs=False, max_length=10000)
        self.satellites_check_address_0 = satellites.check_address('A68MY', "from")
        self.rms_agc_0 = rms_agc(
            alpha=1e-2,
            reference=0.5,
        )
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)

        self.qtgui_sink_x_0.enable_rf_freq(False)



        self.mysat1_100_telemetry_parser_0 = satellites.mysat1_telemetry_parser()
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 7500, 500, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_fcf(5, (firdes.low_pass(1, samp_rate, 1300, 500)), bfo, samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcf(1, (firdes.low_pass(1, samp_rate, 10000, 1000)), bfo, samp_rate)
        self.digital_pfb_clock_sync_xxx_0_0 = digital.pfb_clock_sync_ccf(5, 0.1, (rrc_taps_9k6), nfilts, nfilts/2, 1.5, 2)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(samp_per_sym, 0.05, (rrc_taps), nfilts, nfilts/2, 0.05, 2)
        self.digital_lms_dd_equalizer_cc_0_0_0 = digital.lms_dd_equalizer_cc(2, 0.05, 2, variable_constellation_0)
        self.digital_lms_dd_equalizer_cc_0_0 = digital.lms_dd_equalizer_cc(2, 0.05, 2, variable_constellation_0)
        self.digital_fll_band_edge_cc_0_0 = digital.fll_band_edge_cc(5, 0.350, 100, 0.01)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(samp_per_sym, 0.350, 100, 0.010)
        self.digital_descrambler_bb_0 = digital.descrambler_bb(0x21, 0, 16)
        self.digital_costas_loop_cc_0_0_0_0_0 = digital.costas_loop_cc(0.1, 2, False)
        self.digital_costas_loop_cc_0_0_0_0 = digital.costas_loop_cc(0.1, 2, False)
        self.digital_binary_slicer_fb_0_0 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", '', '52001', 10000, True)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 32767)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blks2_tcp_source_0_0 = grc_blks2.tcp_source(
        	itemsize=gr.sizeof_short*1,
        	addr='10.102.21.44',
        	port=20022,
        	server=False,
        )
        self.analog_feedforward_agc_cc_0_0 = analog.feedforward_agc_cc(1024, 2)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_check_address_0, 'ok'), (self.satellites_print_timestamp_0, 'in'))
        self.msg_connect((self.satellites_hdlc_deframer_0, 'out'), (self.satellites_check_address_0, 'in'))
        self.msg_connect((self.satellites_hdlc_deframer_0_0, 'out'), (self.satellites_check_address_0, 'in'))
        self.msg_connect((self.satellites_pdu_to_kiss_0, 'out'), (self.blocks_socket_pdu_0, 'pdus'))
        self.msg_connect((self.satellites_print_timestamp_0, 'out'), (self.mysat1_100_telemetry_parser_0, 'in'))
        self.msg_connect((self.satellites_print_timestamp_0, 'out'), (self.satellites_pdu_to_kiss_0, 'in'))
        self.msg_connect((self.satellites_print_timestamp_0, 'out'), (self.satellites_submit_0, 'in'))
        self.connect((self.analog_feedforward_agc_cc_0_0, 0), (self.digital_fll_band_edge_cc_0_0, 0))
        self.connect((self.blks2_tcp_source_0_0, 0), (self.blocks_short_to_float_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.digital_binary_slicer_fb_0_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.satellites_nrzi_decode_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_0, 0), (self.satellites_nrzi_decode_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0_0, 0), (self.digital_lms_dd_equalizer_cc_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0_0_0, 0), (self.digital_lms_dd_equalizer_cc_0_0_0, 0))
        self.connect((self.digital_descrambler_bb_0, 0), (self.satellites_hdlc_deframer_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.digital_lms_dd_equalizer_cc_0_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.digital_lms_dd_equalizer_cc_0_0_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0_0_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.digital_costas_loop_cc_0_0_0_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_feedforward_agc_cc_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.rms_agc_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_pfb_clock_sync_xxx_0_0, 0))
        self.connect((self.rms_agc_0, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.satellites_nrzi_decode_0, 0), (self.digital_descrambler_bb_0, 0))
        self.connect((self.satellites_nrzi_decode_0_0, 0), (self.satellites_hdlc_deframer_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "mysat1")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_bfo(self):
        return self.bfo

    def set_bfo(self, bfo):
        self.bfo = bfo
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.bfo)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.bfo)

    def get_callsign(self):
        return self.callsign

    def set_callsign(self, callsign):
        self.callsign = callsign

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_latitude(self):
        return self.latitude

    def set_latitude(self, latitude):
        self.latitude = latitude

    def get_longitude(self):
        return self.longitude

    def set_longitude(self, longitude):
        self.longitude = longitude

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_recstart(self):
        return self.recstart

    def set_recstart(self, recstart):
        self.recstart = recstart

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.samp_per_sym), 0.35, 11*self.samp_per_sym*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps_9k6(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(5), 0.35, 11*5*self.nfilts))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.samp_per_sym), 0.35, 11*self.samp_per_sym*self.nfilts))

    def get_variable_constellation_0(self):
        return self.variable_constellation_0

    def set_variable_constellation_0(self, variable_constellation_0):
        self.variable_constellation_0 = variable_constellation_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 7500, 500, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((firdes.low_pass(1, self.samp_rate, 1300, 500)))
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, 10000, 1000)))

    def get_rrc_taps_9k6(self):
        return self.rrc_taps_9k6

    def set_rrc_taps_9k6(self, rrc_taps_9k6):
        self.rrc_taps_9k6 = rrc_taps_9k6
        self.digital_pfb_clock_sync_xxx_0_0.update_taps((self.rrc_taps_9k6))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.rrc_taps))


def argument_parser():
    description = 'Decodes 1k2/9k6 BPSK + G3RUH telemetry from MYSAT 1'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--bfo", dest="bfo", type="eng_float", default=eng_notation.num_to_str(1.5e3),
        help="Set carrier frequency of the BPSK signal [default=%default]")
    parser.add_option(
        "", "--callsign", dest="callsign", type="string", default='',
        help="Set your callsign [default=%default]")
    parser.add_option(
        "", "--ip", dest="ip", type="string", default='::',
        help="Set UDP listen IP [default=%default]")
    parser.add_option(
        "", "--latitude", dest="latitude", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set latitude (format 00.000 or -00.000) [default=%default]")
    parser.add_option(
        "", "--longitude", dest="longitude", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set longitude (format 00.000 or -00.000) [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="intx", default=7355,
        help="Set UDP port [default=%default]")
    parser.add_option(
        "", "--recstart", dest="recstart", type="string", default='',
        help="Set start of recording, if processing a recording (format YYYY-MM-DD HH:MM:SS) [default=%default]")
    return parser


def main(top_block_cls=mysat1, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(bfo=options.bfo, callsign=options.callsign, ip=options.ip, latitude=options.latitude, longitude=options.longitude, port=options.port, recstart=options.recstart)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
