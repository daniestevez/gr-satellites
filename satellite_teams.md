# A note to satellite teams planning to use gr-satellites

gr-satellites gives a large number of tools that can be reused when developing a
groundstation solution for a small satellite mission, and it is designed with
that goal in mind.

If you are working on a satellite mission (especially if it uses Amateur radio
spectrum) and you are thinking about using some parts of gr-satellites to build
your groundstation, rather than forking off a decoder that only works for your
own satellite, please give some thought to the idea of contributing back to
upstream the changes needed to incorporate support for your satellite in the
upstream gr-satellites version.

In this way, you get for free some advantages, such as a large user base of
Amateur satellite observers and Amateur radio operators already familiar with
the installation and operation of the software, maintainance to keep your
software working with new versions of GNU Radio or future improvements of
gr-satellites (this is especially important if you plan on a short main mission of
a few months but your satellite will continue transmitting afterwards, perhaps
for several years), and other advantages related to forming part of a large
worldwide community.

Additionally, if your satellite uses Amateur radio spectrum, it will eventually
be supported in gr-satellites anyway, since gr-satellites strives to support all
Amateur satellites. Therefore, by collaborating and incorporating your changes
back to upstream, you save me work in adding to gr-satellites support for your
satellite.

Even if you are thinking about using an external tool to process your telemetry,
such as a GUI tool to classify, show and store telemetry values, the
gr_satellites command line tool can easily be connected to such a tool by using
appropriate data sinks with TCP sockets, ZeroMQ or other IPC methods. By using
the upstream gr_satellites command line tool as your decoding backend, you gain
all the support from the community.

So if you are planning to use gr-satellites for something as important as your
next satellite mission, we are glad to have you on-board. You are more than
welcome to write in
[Github issues](https://github.com/daniestevez/gr-satellites/issues)
a heads-up message, such as a statement of interest or presentation letter
(you can make it look the way you like) so that we are aware of your work and can
start coordinating efforts with you.

With gr-satellites, I have been supporting dozens of satellite missions over
more than four years, so I have good experience about which communication
technologies work best, and which work worse. Thus, I am also happy to give
advice if you are in the early planning stages of your mission.

---

Daniel Estévez, gr-satellites lead developer
