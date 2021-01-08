.. _Installing from source:

Installing from source
======================

gr-satellites is a GNU Radio out-of-tree module, and can be installed as such,
by building it from source in a system where GNU Radio is already installed. The
general steps for installing gr-satellites from source include making sure that
all the dependencies are installed and then building and installing the
out-of-tree module.

Dependencies
^^^^^^^^^^^^

gr-satellites requires `GNU Radio`_ version at least 3.8.


.. warning::
   There are some build dependencies for GNU Radio out-of-tree modules that
   are not required to run GNU Radio, so some distributions might not install them
   by default when GNU Radio is installed. The main ones that may cause problems
   are:

   * swig
   * liborc (in Debian-based distributions ``liborc-0.4-dev`` is needed)

Additionally, the following libraries are required:

* `construct`_, at least version 2.9.
* `requests`_

.. note::
   construct and requests are Python packages and can be installed with `pip`_
   by doing

   .. code-block:: console

      $ pip3 install --user --upgrade construct requests

   Alternatively, construct and requests can be installed from your
   distribution's package manager
 
.. _GNU Radio: https://gnuradio.org/
.. _construct: https://construct.readthedocs.io/en/latest/
.. _requests: https://pypi.org/project/requests/
.. _pip: https://pypi.org/project/pip/

Optional dependencies
^^^^^^^^^^^^^^^^^^^^^

To use the realtime image decoders, gr-satellites needs `feh`_

.. _feh: https://feh.finalrewind.org/

.. note::
   feh is best installed through your distribution's package manager

The decoders that use Mobitex or Mobitex-NX require the GNU Radio out-of-tree
module ``gr-tnc_nx``, which can be found in `beesat-sdr`_ (note that the
``maint-3.8`` branch is the one which supports GNU Radio 3.8).

.. _beesat-sdr: https://github.com/daniestevez/beesat-sdr/tree/maint-3.8
   
Downloading
^^^^^^^^^^^

gr-satellites is developed in the `daniestevez/gr-satellites`_ Github
repository. It is recommended that you download the `latest stable release`_.
You can also browse the list of `all releases`_ to see older vesions
and pre-releases.

Users interested in collaborating with testing or developing gr-satellites can
clone the git repository and use the master branch. There is more information
about the organization in branches in the `README`_.

.. _daniestevez/gr-satellites: https://github.com/daniestevez/gr-satellites/
.. _latest stable release: https://github.com/daniestevez/gr-satellites/releases/latest
.. _all releases: https://github.com/daniestevez/gr-satellites/releases
.. _README: https://github.com/daniestevez/gr-satellites/blob/master/README.md

Building and installing
^^^^^^^^^^^^^^^^^^^^^^^

gr-satellites can be built and installed using cmake. The following can be run
inside the directory containing the gr-satellites sources:

.. code-block:: console

   $ mkdir build
   $ cd build
   $ cmake ..
   $ make
   $ sudo make install
   $ sudo ldconfig

After running ``make``, you can run the tests by doing ``make test`` in the
``build/`` directory.

.. note::
   There are systems where the AO-73 and similar decoders fail to decode correctly if
   ``volk_profile`` has not been run ever in the system. This seems to be caused
   by the Viterbi decoder chosen by Volk by default when there is no
   ``~/.volk/volk_config`` file. If problems with these decoders are seen, it
   is recommended to run ``volk_profile`` to see if it fixes the problems. Additionally,
   it is recommended to check if in ``~/.volk/volk_config`` there is a line that
   contains ``volk_8u_x4_conv_k7_r2_8u avx2 avx2`` and replace both occurences
   of ``avx2`` by either ``spiral`` or ``generic``.


PYTHONPATH
^^^^^^^^^^

After installing gr-satellites, it is necessary to ensure that Python is able
to locate the gr-satellites Python module. Depending on the configuration of
Python and the location where gr-satellites has been installed, it might be
necessary to set the ``PYTHONPATH`` environment variable.

If Python is not able to locate the gr-satellites module, it will produce an
error like this:

.. code-block:: python

   ModuleNotFoundError: No module named 'satellites'

Often, gr-satellites is installed into ``/usr/local/lib/python3/dist-packages/``
or a similar directory, in a subdirectory called ``satellites``. Therefore,

.. code-block:: console

   $ export PYTHONPATH=/usr/local/lib/python3/dist-packages/

can be used to allow Python to find the gr-satellites module. More information
about the ``PYTHONPATH`` can be found in Python's documentation description of
the `PYTHONPATH`_.

.. note::
   A permanent configuration of the ``PYTHONPATH`` can be added to a script such as
   ``~/.bashrc`` or ``~/.bash_profile``. This applies the correct
   ``PYTHONPATH`` when ``gr_satellites`` or ``gnuradio-companion`` are run from
   a ``bash`` session. If ``gnuradio-companion`` is run directly from the
   graphical environment, then it is necessary to set the ``PYTHONPATH`` in
   xinitrc or xprofile. See the
   `Arch Linux documentation on environment variables`_
   for more information,

.. _PYTHONPATH: https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH
.. _Arch Linux documentation on environment variables: https://wiki.archlinux.org/index.php/Environment_variables

.. _Downloading sample recordings:

Downloading sample recordings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``satellite-recordings/`` directory is a `git submodule`_ that contains many
short sample recordings of different satellites that can be used to test the
decoders. From a clone of the gr-satellites git repository, the submodule can
be cloned (downloaded) by running

.. code-block:: console

   $ git submodule update --init

inside the ``gr-satellites/`` directory.

Alternatively, it is possible to run

.. code-block:: console

   $ git clone --recursive https://github.com/daniestevez/gr-satellites

when cloning the gr-satellites repository to download both gr-satellites and the
satellite-recordings submodule.

The satellite-recordings sample recordings can also be downloaded from its
`own git repository <https://github.com/daniestevez/satellite-recordings/>`_,
which is necessary if gr-satellite has not been installed from the git repository.

.. _git submodule: https://git-scm.com/book/en/v2/Git-Tools-Submodules
