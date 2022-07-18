###############
testdata_ci_hsc
###############

``testdata_ci_hsc`` provides a minimum amount of test data sufficient to run the LSST Science Pipelines `ci_hsc`_ tests from single frame processing through coaddition processing, based on engineering test data from Hyper Suprime-Cam.

.. _ci_hsc: https://github.com/lsst/ci_hsc/

Contents of this package
========================

A clone of this package will take about 8GB of disk space: about 3.5GB of calibrations, 400MB of raw files, and their git LFS copies.

raw files
---------

The ``raw/`` directory contains 33 raw files, with these corresponding dataIds in the butler repo that is created during a run of `ci_hsc`_.
Run this butler command on a successful `ci_hsc`_ run to get a similar table::

    butler query-data-ids --collections HSC/runs/ci_hsc --datasets src DATA exposure detector


.. _table-dataIds:

.. table:: included dataIds

+------+-----------------+----------------+-----------------+
| band | physical_filter | exposure/visit | detectors       |
+======+=================+================+=================+
| r    | HSC-R           | 903334         | 16, 22, 23, 100 |
+------+-----------------+----------------+-----------------+
| r    | HSC-R           | 903336         | 17, 24          |
+------+-----------------+----------------+-----------------+
| r    | HSC-R           | 903338         | 18, 25          |
+------+-----------------+----------------+-----------------+
| r    | HSC-R           | 903342         | 4, 10, 100      |
+------+-----------------+----------------+-----------------+
| r    | HSC-R           | 903344         | 0, 5, 11        |
+------+-----------------+----------------+-----------------+
| r    | HSC-R           | 903346         | 1, 6, 12        |
+------+-----------------+----------------+-----------------+
| i    | HSC-I           | 903986         | 16, 22, 23, 100 |
+------+-----------------+----------------+-----------------+
| i    | HSC-I           | 903988         | 16, 17, 23, 24  |
+------+-----------------+----------------+-----------------+
| i    | HSC-I           | 903990         | 18, 25          |
+------+-----------------+----------------+-----------------+
| i    | HSC-I           | 904010         | 4, 10, 100      |
+------+-----------------+----------------+-----------------+
| i    | HSC-I           | 904014         | 1, 6, 12        |
+------+-----------------+----------------+-----------------+

calibrations
------------

The ``calib/`` directory contains files for brighter-fatter, bias, dark, flat, sky frame, and defect correction, plus a database defining their validity ranges.

The ``jointcal/`` directory contains jointcal output files from a full-focal plane run of jointcal astrometry and photometry.
These files are used to apply external jointcal calibrations during coadd processing, as there is not enough data in this package to reliably run jointcal on directly.

Reference catalog
-----------------

Reference catalogs for astrometry and photometry are included in the ``gaia_dr2_20200414/`` and ``ps1_pv3_3pi_20170110/`` directories, respectively.
Only the relevant HTM shards that apply to the above detector/visits are included.
See the ``README.txt`` files in those directories for details.
They are automatically loaded during the appropriate steps of ``ci_hsc``'s processing.

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

git lfs
=======

The data used by ``ci_hsc`` is stored using `Git LFS`_; refer to the `relevant LSST documentation`_ for details on how to check out this repository.

.. _Git LFS: https://git-lfs.github.com
.. _relevant LSST documentation: http://developer.lsst.io/en/latest/tools/git_lfs.html
