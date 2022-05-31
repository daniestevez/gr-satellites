# QO-100 multimedia beacon receiver

## Description

This folder contains an example of a QO-100 multimedia beacon receiver using
some blocks from gr-satellites.

The main part of the receiver is included in the hierarchical flowgraph
`qo100_multimedia_beacon.grc`. The input of this flowgraph is the beacon signal
as IQ data at a nominal sample rate of 6ksps (other sample rates can be used,
but perhaps with worse performance).

This hierarchical flowgraph should be included into a flowgraph that interfaces
with the SDR (or soundcard input) and performs downconversion, filtering and
decimation. It is expected that users will make their own flowgraph according to
the hardware, sample rate and frequency plan of their station. An example is
included in the flowgraph `qo100_multimedia_beacon_ea4gpz.grc`. This gets a
600ksps IQ input using the Linrad network protocol with 10489.750 MHz centred at
DC.

The other element used in the receiver is the Python script
`qo100_websockets_server.py` that runs a WebSockets server. This is used for
sending real-time data from the beacon into a web browser. The beacon transmits
a file `qo100info.html` that can be opened with a web browser. This HTML file
will connect to the WebSockets server to fetch and display real-time data.

## Running

1. Generate the hierarchical flowgrah `qo100_multimedia_beacon.grc` in GNU Radio
Companion (Run > Generate menu). After generating it, restart GNU Radio
Companion.

2. The QO-100 multimedia beacon RX block should be included in a flowgraph
that interfaces with the SDR. See `qo100_multimedia_beacon_ea4gpz.grc` for an
example.

3. Run the flowgraph and the `qo100_websockets_server.py` script. They can be
started in any order, and restarted independently.

4. Check that a good 8APSK constellation is displayed in the GUI of the
flowgraph.

5. Wait some minutes for the the file `qo100info.html` to be received. This will
appear in `/tmp` by default (the location where files are saved can be changed in
the parameters of the QO-100 multimedia beacon RX block).

6. Open the file `qo100info.html` in a web browser. The web page should display
the message "CONNECTED to local HSModem" in green rather than "offline" in
red. Real-time information, such as the waterfall data will start to appear in
the web page.
