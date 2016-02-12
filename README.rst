==========
``ci_hsc``
==========

``ci_hsc`` provides test data and script which exercises the LSST stack
through single frame and coadd processing based on engineering test data from
Hyper Suprime-Cam.

Obtaining test data
===================

The data used by ``ci_hsc`` is stored using `Git LFS`_; refer to the `relevant
LSST documentation`_ for details on how to check out this repository.

.. _Git LFS: https://git-lfs.github.com
.. _relevant LSST documentation: http://developer.lsst.io/en/latest/tools/git_lfs.html

Running the tests
=================

Set up the package
------------------

The package must be set up in the usual way before running::

  $ cd ci_hsc
  $ setup -j -r .

Reference catalog
-----------------

An appropriate astrometric reference catalog is provided in the
``sdss-dr9-fink-v5b`` directory. It must be declared to `EUPS`_ and set up
before using this package::

  $ eups declare -r ${CI_HSC_DIR}/sdss-dr9-fink-v5b astrometry_net_data sdss-ci_hsc
  $ setup -j astrometry_net_data sdss-ci_hsc

.. _EUPS: https://github.com/RobertLuptonTheGood/eups

Running the tests
-----------------

Execute ``scons``. On a Mac running OSX 10.11 or greater, you must specify a
Python interpreter followed by a full path to ``scons``::

  $ python $(which scons)

On other systems, simply running ``scons`` should be sufficient.
