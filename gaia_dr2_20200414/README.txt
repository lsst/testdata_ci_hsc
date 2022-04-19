This is a pared-down version of the gaia_dr2_20200414 reference catalog,
for astrometry with the LSST ci_hsc package, containing the following shards:

    189584 189648


Reference Catalog: Gaia DR2
###########################

Sky coverage: full sky
Number of sources: 1,692,919,135
Magnitude range: ~7 - 21.4 (G magnitude)
Disk space: 310 GB

Original data: https://www.cosmos.esa.int/web/gaia/dr2
Jira Epic: https://jira.lsstcorp.org/browse/DM-19473
Jira acceptance RFC: https://jira.lsstcorp.org/browse/RFC-634
Contact: John Parejko, parejkoj@uw.edu, Slack: parejkoj

The full Gaia DR2 catalog in indexed HTM format. This is the first LSST refcat
to contain coordinate errors, proper motions, and parallaxes.

Citations/acknowledgements
==========================

Users of this reference catalog should follow the citation and acknowledgement
instructions from this website:
https://gea.esac.esa.int/archive/documentation/GDR2/Miscellaneous/sec_credit_and_citation_instructions/

Catalog creation
================

This refcat was created with a specialized subclass of
`IngestIndexedReferenceTask` created to handle the gaia instrumental fluxes:
`IngestGaiaReferenceTask`.

To re-create this catalog, download the complete gaia_source DR2 files from
the Gaia Archive (~550 GB total) in CSV format:
http://cdn.gea.esac.esa.int/Gaia/gdr2/gaia_source/

Follow these instructions, noting the substitution of `IngestGaiaReferenceTask`
for the base-class `IngestIndexedReferenceTask`:
https://pipelines.lsst.io/v/w_2019_42/modules/lsst.meas.algorithms/creating-a-reference-catalog.html

The configuration that was used to ingest the data is included in this
directory as `IngestIndexedReferenceTask.py`.
