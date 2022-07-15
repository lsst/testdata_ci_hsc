==========
``testdata_ci_hsc``
==========

``testdata_ci_hsc`` provides the minimum required amount of test data that is
sufficient to run the LSST software stack from single frame processing through
coaddition processing.


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

This package provides the test data for the `ci_hsc`_ package: both this and `ci_hsc`_ must be setup in eups in order to run the tests in `ci_hsc`_.
One way to accomplish this is as follows::

  $ cd testdata_ci_hsc
  $ setup -r .
  $ cd PATH_TO_CI_HSC
  $ setup -kr .

Reference catalog
-----------------

An appropriate reference catalog for both astrometry and photometry is
provided in the ``ps1_pv3_3pi_20170110`` directory. See the ``README.txt``
file in that directory for details. It is automatically enabled by the default
HSC processing configuration.
