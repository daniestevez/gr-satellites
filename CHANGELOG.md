# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
- Support for AALTO-1 CC1125 mode
- Support for Grizu-263A
- Support for UVSQ-SAT
- Example decoder for NEXUS 19k2 pi/4-DQPSK telemetry
- Support for MiTEE-1
- Preliminary support for CAPE-3 (only ASFK AX.25)
- Support for EXOCUBE-2
- PDU Length Filter block
- Support for IDEASSat
- Support for SOMP 2b

### Changed
- Add filter before quadrature demod for IQ input FSK demodulator

### Fixed
- Runtime error when the baudrate is too high for the sample rate
- Build problems with clang
- Errors about wrong Reed-Solomon message size with OPS-SAT deframer

## [3.6.0] - 2020-12-04

### Added
- PDU add metadata block
- PDU Head/Tail block
- Lucky-7 image receiver
- Support for custom SIDS servers
- Support for AISTECHSAT-2 custom protocol
- Support for BOBCAT-1
- Support for BY03
- Support for FossaSat-1B and FossaSat-2
- Support for NEUTRON-1
- Support for SPOC
- Support for TTU-100
- Support for VZLUSAT-2

### Changed
- Replaced boost::bind() by C++ lambdas
- Refactored Reed-Solomon decoder C++ blocks
- Refactored CCSDS deframer blocks to allow more generality
- Make --clk_limit parameter relative to samples per symbol
- Updated AISTECHSAT-2 transmit frequency
- Definitive NORAD IDs for NETSAT 1-4

### Removed
- Deprecated Astrocast 9k6 deframer in favour of the new CCSDS Reed-Solomon deframer
- Deprecated CC11xx remove length, Header remover and Strip AX.25 header in favour of PDU Head/Tail

## [3.5.2] - 2020-10-21

### Changed
- Fixed bug in S-NET deframer

## [3.5.1] - 2020-10-17

### Changed
- Added final NORAD ID for DEKART
- Fixed bug in SALSAT CRC calculation

## [3.5.0] - 2020-10-08

### Added
- Option for generating correct recording timestamps by playing back at 1x speed
- Option for listing the supported satellites in gr_satellites
- Mobitex and Mobitex-NX deframer
- Support for SALSAT
- Support for MEZNSAT
- Support for satellites using Mobitex and Mobitex-NX (D-STAR ONE, BEESAT, TECHNOSAT,
  AMGU-1, SOKRAT, DEKART)
- Support for NETSAT 1, 2, 3, 4
- Support for NORBI
- Support for KAIDUN-1

### Fixed
- Bug with Reed-Solomon decoder that prevented building on i386 since v3.3.0

## [3.4.0] - 2020-09-12

### Added
- SatYAML file for STRAND-1
- Audio source in gr_satellites
- SatYAML file for AmicalSat
- SatYAML file for UPMSat 2
- Support for NASA-DSN convention in CCSDS concatenated frames
- Support for TRISAT
- TCP KISS server and ZMQ PUB socket to send decoded frames	
- CSP fragmentation flag
- SatYAML file for ION-MK01

### Changed
- Enable full printing of construct strings

## [3.3.0] - 2020-08-11

### Added
- Documentation for installing with conda
- SatYAML file for GO-32
- KISS output from gr_satellites and the KISS file sink includes timestamps
- Support for building with MSVC in Windows

### Changed
- Telemetry conversion formulas for BY02
- JY1SAT SSDV decoder utility now uses KISS files as input
- Removed dependence on libfec. The Reed-Solomon codes from libfec are now included in gr-satellites.
- Added 4k8 modulation to SpooQy-1

### Fixed
- Bug in Telemetry parser block when used from GRC
- Delphini-1 SatYAML file
- Stray line in Lucky7 deframer GRC block

## [3.2.0] - 2020-07-14

### Added
- Option not to add a control byte in PDU to KISS
- Connection to the Harbin Institute of Technology telemetry proxy from Telemetry Submit

### Fixed
- Bug that prevented the NORAD field from appearing in Telemetry Submit

## [3.1.0] - 2020-07-11

### Added
- Example flowgraphs from gr-kiss
- Support for CAS-6
- Option to disable scrambler in CCSDS deframers
- Note about volk_profile in the documentation
- Missing .yml grc file for LilacSat-1 deframer
- Support for BY02
- Command line options for satellite decoder block and components
- More documentation about --dump_path

### Changed
- Do not use DC-block in AFSK demodulator
- Remove second lowpass filter in BPSK demodulator
- Improvements in LilacSat-1 demuxer and deframer
- Ported NRZI encoder and decoder to C++
- Re-encode frame in SMOG-P RA decoder to check decoding correctness

### Fixed
- Cmake warning when searching for libfec
- Minor corrections to documentation
- Bug in HDLC Framer

### Removed
- Deprecated SMOG-P packet filter block

## [3.0.0] - 2020-06-03

Changes from 3.0.0-rc1

### Added
- Download instructions in documentation
- Support for AO-27
- Support for FALCONSAT-3
- Test for unknown keywords in SatYAML files

### Fixed
- Test execution in gr-satellites is not yet installed
- Minor typos in documentation
- Added missing af_carrier to AFSK SatYAML files
- swig and PythonLibs are now mandatory when running cmake
- Missing import in AFSK demodulator

### Removed
- Deprecated LilacSat-2 flowgraphs in apps/

## [3.0.0-rc1] - 2020-05-17

Large refactor release bringing new functionality and improvements. This is an overview of the main changes:

### Added
- gr_satellites command line tool
- Satellite decoder block
- Components
- SatYAML files
- File and image receiver
- Sphinx Documentation

### Changed
- Performance improvements to the demodulators

### Removed
- A number of deprecated low level blocks

## [2.3.2] - 2020-05-16
### Fixed
- Bug in telemetry submitter caused by HTTP 400 error

## [2.3.1] - 2020-04-11
### Fixed
- Bug in FUNcube telemetry parser

## [2.3.0] - 2020-02-05
### Added
- Support for SMOG-P and ATL-1 at 2500 and 12500 baud
- Support for construct 2.10
### Fixed
- Bug with DC block and AGC of SMOG-P and ATL-1 potentially causing crashes

## [2.2.0] - 2020-01-01
### Added
- Support for SMOG-P and ATL-1
- Support for DUCHIFAT-3
- Support for OPS-SAT
- Standanlone decoder for AAUSAT-4
- Support for FloripaSat-1
- BME telemetry forwarder
### Changed
- Replaced AO-40 synchronizer by more general distributed synchronizer
- Replaced AO-40 deinterleaver by more general matrix deinterleaver

## [2.1.0] - 2019-11-01
### Added
- Support for Luojia-1
### Fixed
- Corrected FACSAT NORAD ID

## [2.0.0] - 2019-10-10
### Added
- Support for GNU Radio 3.8
- Support for 4k8 in ESEO decoder

### Removed
- Support for GNU Radio 3.7

## [1.8.1] - 2019-10-07
### Fixed
- Bug with FUNcube telemetry submitter in some flowgraphs

## [1.8.0] - 2019-10-04
### Added
- Światowid image decoder
- Support for Taurus-1
- CCSDS blocks from SOCIS

### Fixed
- KISS and HDLC blocks from gr-kiss in some flowgraphs

## [1.7.0] - 2019-08-31
### Added
- Support for EntrySat
- Support for Delphini-1
- Support for AmGU-1
- Support for Sokrat
- Support for BEESAT-9
- Support for Lucky-7
- Support for Światowid 9k6 protocol

### Removed
- Telemetry submitter for EntrySat

### Fixed
- Bug in FUNcube telemetry parsing

## [1.6.0] - 2019-07-05
### Added
- Support for SpooQy-1
- Generic 1k2 AFSK AX.25 decoder

### Fixed
- Bug in AAUSAT-4 decoder

### Removed
- SatNOGS telemetry forwarders for satellites not coordinated by IARU

## [1.5.0] - 2019-05-01
### Added
- Support for AISTECHSAT-3
- JY1SAT SSDV decoder
- Support for MYSAT 1

### Fixed
- Bugs in FUNcube telemetry parser

## [1.4.0] - 2019-04-07
### Added
- Support for 1KUNS-PF in 9k6 mode
- Support for AISTECH-2
- Support for EQUiSat
- Support for QO-100
- Support for AstroCast 0.1 new protocol and 9k6 mode

### Fixed
- Bugs regarding malformed or unknown frames in Funcube tlm decoder

## [1.3.1] - 2019-01-06
### Fixed
- Bug in the Reed-Solomon decoder (affects ESEO decoder)

## [1.3.0] - 2019-01-05
### Added
- Support for FMN-1
- Support for Shaonian Xing
- Support for Zhou Enlai
- Support for TY 4-01
- Support for FACSAT-1
- Support for INNOSAT-2
- Support for Reaktor Hello World
- CC110x decoder
- Support for 3CAT-1
- Generic FSK AX.25 decoders
- Support for JY1-Sat
- Support for Suomi 100
- Support for PW-Sat2
- Support for ESEO
- Generic Reed-Solomon decoder
- FUNcube telemetry submitter
- Support for ITASAT 1
- Support for D-STAR One
- Support for Astrocast 0.1
- Support for LUME-1

### Changed
- Update to construct 2.9

### Fixed
- Miscellaneous bugs

## [1.2.0] - 2018-09-20
### Added
- feh fullscreen parameter for image decoders

## [1.1.0] - 2018-09-01
### Added
- Support for TANUSHA-3 PM
- 9k6 support for ExAlta-1
- Some extra checks in LilacSat-1 image decoder

## [1.0.0] - 2018-08-02
First gr-satellites release using semantic versioning

[Unreleased]: https://github.com/daniestevez/gr-satellites/compare/v3.6.0...master
[3.6.0]: https://github.com/daniestevez/gr-satellites/compare/v3.5.2...v3.6.0
[3.5.2]: https://github.com/daniestevez/gr-satellites/compare/v3.5.1...v3.5.2
[3.5.1]: https://github.com/daniestevez/gr-satellites/compare/v3.5.0...v3.5.1
[3.5.0]: https://github.com/daniestevez/gr-satellites/compare/v3.4.0...v3.5.0
[3.4.0]: https://github.com/daniestevez/gr-satellites/compare/v3.3.0...v3.4.0
[3.3.0]: https://github.com/daniestevez/gr-satelliites/compare/v3.2.0...v3.3.0
[3.2.0]: https://github.com/daniestevez/gr-satellites/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/daniestevez/gr-satellites/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/daniestevez/gr-satellites/compare/v3.0.0-rc1...v3.0.0
[3.0.0-rc1]: https://github.com/daniestevez/gr-satellites/compare/v2.3.2...v3.0.0-rc1
[2.3.2]: https://github.com/daniestevez/gr-satellites/compare/v2.3.1...v2.3.2
[2.3.1]: https://github.com/daniestevez/gr-satellites/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/daniestevez/gr-satellites/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/daniestevez/gr-satellites/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/daniestevez/gr-satellites/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/daniestevez/gr-satellites/compare/v1.8.1...v2.0.0
[1.8.1]: https://github.com/daniestevez/gr-satellites/compare/v1.8.0...v1.8.1
[1.8.0]: https://github.com/daniestevez/gr-satellites/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/daniestevez/gr-satellites/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/daniestevez/gr-satellites/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/daniestevez/gr-satellites/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/daniestevez/gr-satellites/compare/v1.3.1...v1.4.0
[1.3.0]: https://github.com/daniestevez/gr-satellites/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/daniestevez/gr-satellites/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/daniestevez/gr-satellites/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/daniestevez/gr-satellites/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/daniestevez/gr-satellites/releases/tag/v1.0.0
