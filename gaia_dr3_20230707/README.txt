This is a pared-down version of the gaia_dr3_20230707 reference catalog,
for astrometry with the LSST ci_hsc package, containing the following shards:

    189584 189648


Reference Catalog: Gaia DR3
###########################

Sky coverage: full sky
Number of sources: 1,811,709,771
Magnitude range: ~3 - 21 (G magnitude)
Disk space: 310 GB

Original data: https://www.cosmos.esa.int/web/gaia/dr3
Contact: Clare Saunders, cmsaunders@princeton.edu Slack: cmsaunders

The full Gaia DR3 catalog in indexed HTM format. This is the first LSST refcat
to contain the full coordinate covariance.

Citations/acknowledgements
==========================

Users of this reference catalog should follow the citation and acknowledgement
instructions from this website:
https://gea.esac.esa.int/archive/documentation/GDR3/Miscellaneous/sec_credit_and_citation_instructions/

Catalog creation
================

This refcat was created with a specialized subclass of `ConvertRefcatManager`
created to handle the gaia instrumental fluxes: `ConvertGaiaManager`.

To re-create this catalog, download the complete gaia_source DR3 files from
the Gaia Archive (~550 GB total) in CSV format:
http://cdn.gea.esac.esa.int/Gaia/gdr3/gaia_source/

Follow these instructions, noting the substitution of `ConvertGaiaManager`
for the base-class `ConvertRefcatManager`:
https://pipelines.lsst.io/v/daily/modules/lsst.meas.algorithms/creating-a-reference-catalog.html

The configuration that was used to ingest the data is included in this
directory as `convertReferenceCatalogConfig.py`.
