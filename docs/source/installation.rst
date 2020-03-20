Installation
============

gr-satellites is a GNU Radio out-of-tree module, and it should be installed as
such. The general steps for installing gr-satellites include making sure that
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
   * liborc (in Debian-based distributions ``liborc-0.4-0-dev`` is needed)

Additionally, the following libraries are required:

* `libfec`_
* `construct`_, at least version 2.9.
* `requests`_

.. note::
   libfec can be built and installed from its git repository by doing

   .. code-block:: console

      $ git checkout https://github.com/quiet/libfec
      $ cd libfec
      $ mkdir build
      $ cmake ..
      $ make
      $ sudo make install

   construct and requests are Python packages and can be installed with `pip`_
   by doing

   .. code-block:: console

      $ pip install --user --upgrade construct requests

   Alternatively, construct and requests can be installed from your
   distribution's package manager
 
.. _GNU Radio: https://gnuradio.org/
.. _libfec: https://github.com/quiet/libfec
.. _construct: https://construct.readthedocs.io/en/latest/
.. _requests: https://pypi.org/project/requests/
.. _pip: https://pypi.org/project/pip/

Optional dependencies
^^^^^^^^^^^^^^^^^^^^^

To use the realtime image decoders, gr-satellites needs `feh`_

.. _feh: https://feh.finalrewind.org/

.. note::
   feh is best installed through your distribution's package manager

Building and installing
^^^^^^^^^^^^^^^^^^^^^^^

gr-satellites can be built and installed using cmake:

.. code-block:: console

   $ mkdir build
   $ cd build
   $ cmake ..
   $ make
   $ sudo make install

After running ``make``, you can run the tests by doing ``make test`` in the
``build/`` directory.

		
