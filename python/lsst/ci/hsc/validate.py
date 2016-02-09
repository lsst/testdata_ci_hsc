__all__ = ["RawValidation", "DetrendValidation", "SfmValidation", "SkymapValidation", "WarpValidation",
           "CoaddValidation", "DetectionValidation", "MergeDetectionsValidation", "MeasureValidation",
           "MergeMeasurementsValidation", "ForcedValidation",]

import os
from lsst.pex.logging import getDefaultLog
from lsst.daf.persistence import Butler

_butler = {}
def getButler(root):
    if not root in _butler:
        _butler[root] = Butler(root)
    return butler[root]


class Validation(object):
    _datasets = [] # List of datasets to check we can read
    _files = [] # List of datasets to check that file exists
    _sourceDataset = None # Dataset name of source catalog
    _minSources = 100 # Minimum number of sources
    _matchDataset = None # Dataset name of matches
    _minMatches = 10 # Minimum number of matches
    _butler = {}

    def __init__(self, root, log=None):
        if log is None:
            log = getDefaultLog()
        self.log = log
        self.root = root
        self._butler = None

    @property
    def butler(self):
        if not self._butler:
            self._butler = Butler(self.root)
        return self._butler

    def assertTrue(self, description, success):
        logger = self.log.info if success else self.log.fatal
        logger("%s: %s" % (description, "PASS" if success else "FAIL"))
        if not success:
            raise AssertionError("Failed test: %s" % description)

    def assertFalse(self, description, success):
        self.assertTrue(description, not success)

    def assertEqual(self, description, obj1, obj2):
        self.assertTrue(description + " (%s = %s)" % (obj1, obj2), obj1 == obj2)

    def assertGreater(self, description, num1, num2):
        self.assertTrue(description + " (%d > %d)" % (num1, num2), num1 > num2)

    def assertLess(self, description, num1, num2):
        self.assertTrue(description + " (%d < %d)" % (num1, num2), num1 < num2)

    def assertGreaterEqual(self, description, num1, num2):
        self.assertTrue(description + " (%d >= %d)" % (num1, num2), num1 >= num2)

    def assertLessEqual(self, description, num1, num2):
        self.assertTrue(description + " (%d <= %d)" % (num1, num2), num1 <= num2)

    def validateDataset(self, dataId, dataset):
        self.assertTrue("%s exists" % dataset, self.butler.datasetExists(datasetType=dataset, dataId=dataId))
        # Just warn if we can't load a PropertySet or PropertyList; there's a known issue
        # (DM-4927) that prevents these from being loaded on Linux, with no imminent resolution.
        mappable = self.butler.mapper.datasets.get(dataset, None)
        if mappable is not None and mappable.persistable.startswith("Property"):
            try:
                data = self.butler.get(dataset, dataId)
                self.assertTrue("%s readable (%s)" % (dataset, data.__class__), data is not None)
            except:
                self.log.warn("Unable to load '%s'; this is likely DM-4927." % dataset)
            return
        data = self.butler.get(dataset, dataId)
        self.assertTrue("%s readable (%s)" % (dataset, data.__class__), data is not None)

    def validateFile(self, dataId, dataset):
        filename = self.butler.get(dataset + "_filename", dataId)[0]
        self.assertTrue("%s exists on disk" % dataset, os.path.exists(filename))
        self.assertGreater("%s has non-zero size" % dataset, os.stat(filename).st_size, 0)

    def validateSources(self, dataId):
        src = self.butler.get(self._sourceDataset, dataId)
        self.assertGreater("Number of sources", len(src), self._minSources)
        return src

    def validateMatches(self, dataId):
        # XXX lsst.meas.astrom.readMatches is gone!
        return
        matches = measAstrom.readMatches(self.butler, dataId,)
        self.assertGreater("Number of matches", len(matches), self._minMatches)

    def run(self, dataId, **kwargs):
        if kwargs:
            dataId = dataId.copy()
            dataId.update(kwargs)

        for ds in self._datasets:
            self.log.info("Validating dataset %s for %s" % (ds, dataId))
            self.validateDataset(dataId, ds)

        for f in self._files:
            self.log.info("Validating file %s for %s" % (f, dataId))
            self.validateFile(dataId, f)

        if self._sourceDataset is not None:
            self.log.info("Validating source output for %s" % dataId)
            self.validateSources(dataId)

        if self._matchDataset is not None:
            self.log.info("Validating matches output for %s" % dataId)
            self.validateMatches(dataId)

    def scons(self, *args, **kwargs):
        """Strip target,source,env from scons' call"""
        kwargs.pop("target")
        kwargs.pop("source")
        kwargs.pop("env")
        return self.run(*args, **kwargs)


class RawValidation(Validation):
    _datasets = ["raw"]

class DetrendValidation(Validation):
    _datasets = ["bias", "dark", "flat"]

class SfmValidation(Validation):
    _datasets = ["processCcd_config", "processCcd_metadata", "calexp", "calexpBackground",
                 "icSrc", "icSrc_schema", "src_schema"]
    _sourceDataset = "src"
    _matchDatasets = ["icMatch", "srcMatch"]

class SkymapValidation(Validation):
    _datasets = ["deepCoadd_skyMap"]

class WarpValidation(Validation):
    _datasets = ["deepCoadd_tempExp", "deep_makeCoaddTempExp_config", "deep_makeCoaddTempExp_metadata"]

class CoaddValidation(Validation):
    _datasets = ["deepCoadd", "deep_safeClipAssembleCoadd_config", "deep_safeClipAssembleCoadd_metadata"]

class DetectionValidation(Validation):
    _datasets = ["deepCoadd_det_schema", "detectCoaddSources_config", "detectCoaddSources_metadata"]
    _sourceDataset = "deepCoadd_det"

class MergeDetectionsValidation(Validation):
    _datasets = ["mergeCoaddDetections_config", "deepCoadd_mergeDet_schema"]
    _sourceDataset = "deepCoadd_mergeDet"

class MeasureValidation(Validation):
    _datasets = ["measureCoaddSources_config", "measureCoaddSources_metadata", "deepCoadd_meas_schema"]
    _sourceDataset = "deepCoadd_meas"
    _matchDataset = "deepCoadd_srcMatch"

    def validateSources(self, dataId):
        catalog = Validation.validateSources(self, dataId)
        self.assertTrue("calib_psfCandidate field exists in deepCoadd_meas catalog",
                        "calib_psfCandidate" in catalog.schema)
        self.assertTrue("calib_psfUsed field exists in deepCoadd_meas catalog",
                        "calib_psfUsed" in catalog.schema)

class MergeMeasurementsValidation(Validation):
    _datasets = ["mergeCoaddMeasurements_config", "deepCoadd_ref_schema"]
    _sourceDataset = "deepCoadd_ref"

class ForcedValidation(Validation):
    _datasets = ["deepCoadd_forced_src_schema", "deepCoadd_forced_config", "deepCoadd_forced_metadata"]
    _sourceDataset = "deepCoadd_forced_src"

