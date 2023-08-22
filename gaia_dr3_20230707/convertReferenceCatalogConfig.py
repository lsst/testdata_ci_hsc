import lsst.meas.algorithms.convertReferenceCatalog
assert type(config)==lsst.meas.algorithms.convertReferenceCatalog.ConvertReferenceCatalogConfig, 'config is of type %s.%s instead of lsst.meas.algorithms.convertReferenceCatalog.ConvertReferenceCatalogConfig' % (type(config).__module__, type(config).__name__)
import lsst.meas.algorithms.convertRefcatManager
import lsst.meas.algorithms.indexerRegistry
import lsst.meas.algorithms.readTextCatalogTask
# Version number of the persisted on-disk storage format.
# Version 0 had Jy as flux units (default 0 for unversioned catalogs).
# Version 1 had nJy as flux units.
# Version 2 had position-related covariances.
config.dataset_config.format_version=2

# Name of this reference catalog; this should match the name used during butler ingest.
config.dataset_config.ref_dataset_name='gaia_dr3_20230707'

# Depth of the HTM tree to make.  Default is depth=7 which gives ~ 0.3 sq. deg. per trixel.
config.dataset_config.indexer['HTM'].depth=7

config.dataset_config.indexer.name='HTM'
# Number of python processes to use when ingesting.
config.n_processes=2

config.manager.retarget(target=lsst.meas.algorithms.convertRefcatManager.ConvertGaiaManager, ConfigClass=lsst.meas.algorithms.convertRefcatManager.ConvertRefcatManagerConfig)

# Number of lines to skip when reading the text reference file.
config.file_reader.header_lines=1000

# An ordered list of column names to use in ingesting the catalog. With an empty list, column names will be discovered from the first line after the skipped header lines.
config.file_reader.colnames=[]

# Delimiter to use when reading text reference files.  Comma is default.
config.file_reader.delimiter=','

# Format of files to read, from the astropy.table I/O list here:http://docs.astropy.org/en/stable/io/unified.html#built-in-table-readers-writers
config.file_reader.format='csv'

# A list giving [<match_string>, <fill_value>], which is used to mask the given values in the input file. '0' is suggested for the fill value in order to prevent changing the column datatype. The default behavior is to fill empty data with zeros. See https://docs.astropy.org/en/stable/io/ascii/read.html#bad-or-missing-values for more details.Use `replace_missing_floats_with_nan` to change floats to NaN instead of <fill_value>.
config.file_reader.fill_values=['null', '0']

# If True, replace missing data in float columns with NaN instead of zero. If `fill_values` is set, this parameter with replace the floats identified as missing by `fill_values`, and the fill value from `fill_values` will be overridden with NaN for floats.
config.file_reader.replace_missing_floats_with_nan=True

# Name of RA column (values in decimal degrees)
config.ra_name='ra'

# Name of Dec column (values in decimal degrees)
config.dec_name='dec'

# Name of RA error column
config.ra_err_name='ra_error'

# Name of Dec error column
config.dec_err_name='dec_error'

# Unit of RA/Dec error fields (astropy.unit.Unit compatible)
config.coord_err_unit='milliarcsecond'

# The values in the reference catalog are assumed to be in AB magnitudes. List of column names to use for photometric information.  At least one entry is required.
config.mag_column_list=['phot_g_mean', 'phot_bp_mean', 'phot_rp_mean']

# A map of magnitude column name (key) to magnitude error column (value).
config.mag_err_column_map={}

# Name of column stating if satisfactory for photometric calibration (optional).
config.is_photometric_name=None

# Name of column stating if the object is resolved (optional).
config.is_resolved_name=None

# Name of column stating if the object is measured to be variable (optional).
config.is_variable_name=None

# Name of column to use as an identifier (optional).
config.id_name='source_id'

# Name of proper motion RA column
config.pm_ra_name='pmra'

# Name of proper motion Dec column
config.pm_dec_name='pmdec'

# Name of proper motion RA error column
config.pm_ra_err_name='pmra_error'

# Name of proper motion Dec error column
config.pm_dec_err_name='pmdec_error'

# Scale factor by which to multiply proper motion values to obtain units of milliarcsec/year
config.pm_scale=1.0

# Name of parallax column
config.parallax_name='parallax'

# Name of parallax error column
config.parallax_err_name='parallax_error'

# Scale factor by which to multiply parallax values to obtain units of milliarcsec
config.parallax_scale=1.0

# Include epoch, proper motions, parallax, and covariances between sky coordinates, proper motion, and parallax in the schema. If true, a custom ``ConvertRefcatManager`` class must exist to compute the output covariances.
config.full_position_information=True

# Name of epoch column
config.epoch_name='ref_epoch'

# Format of epoch column: any value accepted by astropy.time.Time, e.g. 'iso' or 'unix'
config.epoch_format='jyear'

# Scale of epoch column: any value accepted by astropy.time.Time, e.g. 'utc'
config.epoch_scale='tcb'

# Extra columns to add to the reference catalog.
config.extra_col_names=['astrometric_excess_noise']

