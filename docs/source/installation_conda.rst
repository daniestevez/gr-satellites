.. _Installing using conda:

Installing using conda
======================

gr-satellites and GNU Radio can also be installed using
`conda`_, both in Linux and in macOS
(support for installing gr-satellites on Windows through conda might be available in
the future). Conda is an open-source package management for Linux, macOS and
Windows that can install packets and their dependencies in different virtual
environments, independently from the rest of the packets installed in the OS.
This section shows how to install `miniconda`_, GNU Radio, and
gr-satellites from scratch.

Miniconda
^^^^^^^^^

`Miniconda`_ is a minimial installer for conda, so it is the recommended way to
get GNU Radio and gr-satellites quickly running in an OS that does not have
conda already installed. Miniconda can be installed by downloading and running
the installer for the appropriate platform from Miniconda's page. The installer
can be run as a regular user. It does not need root access.

After installing Miniconda, its ``(base)`` virtual environment will be active by
default. This means that ``(base)`` will be shown at the beginning of the
command line prompt and  software will be run from the
version installed in the ``(base)`` virtual environment (when it is installed),
and otherwise from the OS.

Users might prefer to run things from the conda virtual environment only upon
request. To disable the activation of the ``(base)`` environment by default, we
can run

.. code-block:: console

   $ conda config --set auto_activate_base false

When the ``(base)`` environment is not enabled by default, we can enter it by
running

.. code-block:: console

   $ conda activate base

and exit it by running

.. code-block:: console

   $ conda deactivate

When the ``(base)`` environment is activated, the prompt will start by
``(base)``. The ``(base)`` environment needs to be activated in order to install
applications through conda into this environment, and also to run applications
that have been previously installed in this environment.

GNU Radio
^^^^^^^^^

To install GNU Radio, the ``(base)`` environment (or another conda virtual
environment) needs to be activated as described above. Installing GNU Radio and
all its dependencies is as simple as doing

.. code-block:: console

   $ conda install -c conda-forge gnuradio

Then GNU Radio may be used normally whenever the virtual environment where it
was installed is activated. For instance, it is possible to run

.. code-block:: console

   $ gnuradio-companion

gr-satellites
^^^^^^^^^^^^^

gr-satellites needs to be installed into a virtual environment where GNU Radio
has been previously installed (the ``(base)`` environment, if following the
instructions here). To install gr-satellites and its dependecies, we do

.. code-block:: console

   $ conda install -c conda-forge -c petrush gnuradio-satellites

After installation, the ``gr_satellites`` command line tool might be run as

.. code-block:: console

   $ gr_satellites

(provided that the virtual environment where it was installed is activated) and
blocks from gr-satellites may be used in GNU Radio companion.

It might be convenient to download the
:ref:`sample recordings <Downloading sample recordings>` manually.

Acknowledgments
^^^^^^^^^^^^^^^

Thanks to `Ryan Volz`_ for packaging GNU Radio for Conda and to `Petrus Hyvönen`_
for putting together recipies to install gr-satellites and its dependencies
through Conda.

.. _conda: https://docs.conda.io/en/latest/
.. _miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _Ryan Volz: https://github.com/ryanvolz
.. _Petrus Hyvönen: https://github.com/petrushy
