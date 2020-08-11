.. _Miscellaneous utilities:

Miscellaneous utilities
=======================

Some small utilities are included in gr-satellties. These are described below.

JY1SAT SSDV decoder
^^^^^^^^^^^^^^^^^^^

The JY1SAT SSDV decoder ``jy1sat_ssdv.py`` can be used to extract and decode
SSDV images transmitted by  `JY1SAT`_. To use the decoder, an `ssdv fork`_
supporting the JY1SAT SSDV frame format needs to be installed. The decoder
operates over a KISS file containing JY1SAT frames. The KISS file can be
produced with the ``--kiss_out`` option of ``gr_satellites`` and might contain
information for one or several images collected over one or several passes.


The decoder is run as

.. code-block:: console

   $ jy1sat_ssdv.py frames.kss /tmp/output

This will create files ``/tmp/output_n.ssdv`` with the extracted SSDV frames and
``/tmp/output_n.jpg`` with the decoded JPEG image data, where ``n`` is the
number of the image.

.. _JY1SAT: https://amsat-uk.org/tag/jy1sat/
.. _ssdv fork: https://github.com/daniestevez/ssdv

SMOG-P spectrum plot
^^^^^^^^^^^^^^^^^^^^

The SMOG-P spectrum plot tool ``smog_p_spectrum.py`` can be used to plot
spectrum data files transmitted by `SMOG-P`_ and `ATL-1`_ . These files are
produced by the :ref:`file receiver component <File and Image receivers>`. The
``smog_p_spectrum.py`` script can be run by using the name of the spectrum data
file as argument. For instance,

.. code-block:: console

   $ smog_p_spectrum.py spectrum_start_824000000_step_24000_rbw_6_measid_312

This will create an image ``spectrum_312.png`` in the same directory as the
spectrum file (here ``312`` is the ID of the measurement, and is contained at
the end of the spectrum file name).
   
.. _SMOG-P: https://space.skyrocket.de/doc_sdat/smog-p.htm
.. _ATL-1: https://space.skyrocket.de/doc_sdat/atl-1.htm

