import lsst.meas.algorithms.convertReferenceCatalog
assert type(config)==lsst.meas.algorithms.convertReferenceCatalog.DatasetConfig, 'config is of type %s.%s instead of lsst.meas.algorithms.convertReferenceCatalog.DatasetConfig' % (type(config).__module__, type(config).__name__)
import lsst.meas.algorithms.indexerRegistry
# Version number of the persisted on-disk storage format.
# Version 0 had Jy as flux units (default 0 for unversioned catalogs).
# Version 1 had nJy as flux units.
# Version 2 had position-related covariances.
config.format_version=2

# Name of this reference catalog; this should match the name used during butler ingest.
config.ref_dataset_name='gaia_dr3_20230707'

# Depth of the HTM tree to make.  Default is depth=7 which gives ~ 0.3 sq. deg. per trixel.
config.indexer['HTM'].depth=7

config.indexer.name='HTM'
