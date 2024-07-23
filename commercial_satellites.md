# gr-satellites policy for commercial satellites

The main mission of the gr-satellites project is to provide GNU Radio decoders
for all (or most) satellites that transmit on amateur radio spectrum. This is in
agreement with the self-training and technical experimentation purposes that
define the amateur service in the ITU Radio Regulations, and with the principle
of not encoding amateur transmissions with the purpose of obscuring their
meaning.

gr-satellites can also be a useful tool for commercial satellite missions, and
it is in fact used in several such missions. However, the gr-satellites project
reckons and respects that some commercial satellite operators might not be
approving of amateur radio operators and amateur satellite observers decoding
data transmitted by their satellites (and this act might be illegal in some
jurisdictions).

The gr-satellites project will only accept code contributions (whether in the
form of SatYAML files or GNU Radio blocks) specifically intended for the
reception of a commercial satellite if those contributions are endorsed or
acknowledged by the satellite operator or owner. This restriction only affects
amateurs using gr-satellites to receive commercial satellites. Commercial
satellite operators are encouraged and welcome to upstream code contributions to
gr-satellites regarding their own satellites, if they wish to do so.

Code contributions which are generic in nature, such as GNU Radio blocks that
implement support for a radio that could potentially be used in amateur and
commercial missions, are not affected by this restriction and are always
accepted in gr-satellites.

The gr-satellites project also acknowledges that there exist many satellites
that transmit on amateur radio spectrum that are not amateur in nature, and that
these satellites should not be using amateur spectrum. Some of these satellites
are fully supported by gr-satellites. This is in line with the common practice
of self-monitoring of amateur radio spectrum by amateur operators. Hopefully the
existence of these decoders and a community that uses them to monitor the
missions will be another incentive that makes non-amateur missions avoid using
amateur spectrum in the future. For this reason, gr-satellites will continue
trying to support any satellite that transmits on amateur radio spectrum,
regardless of the nature of the mission, and accepts all contributions to this
end.
