GNURADIO_SOURCE=/usr/src/gnuradio-3.8.0.0/

.PHONY: all
all: test

test: test.cc
	g++ -Wall -O2 -o test test.cc $(GNURADIO_SOURCE)/gr-digital/lib/timing_error_detector.cc $(GNURADIO_SOURCE)/gr-digital/lib/interpolating_resampler.cc -I$(GNURADIO_SOURCE)/gr-digital/lib/ -I$(GNURADIO_SOURCE)/gr-filter/include -lgnuradio-digital -lgnuradio-filter

clean:
	rm -f test
