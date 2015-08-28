
class Validation(object):
    _datasets = [] # List of datasets to check we can read
    _files = [] # List of datasets to check that file exists
    _sourceDataset = None # Dataset name of source catalog
    _minSources = 100 # Minimum number of sources
    _matchDataset = None # Dataset name of matches
    _minMatches = 10 # Minimum number of matches

    def __init__(self, log=None):
        if log is None:
            log = pexLog.getDefaultLog()
        self.log = log

    def assertTrue(self, description, success):
        self.log.write("*** %s: %s\n" % (description, "PASS" if success else "FAIL"))
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

    def validateDataset(self, butler, dataId, dataset):
        self.assertTrue("%s exists" % dataset, butler.datasetExists(datasetType=dataset, dataId=dataId))
        data = butler.get(dataset, dataId)
        self.assertTrue("%s readable (%s)" % (dataset, data.__class__), data)

    def validateFile(self, butler, dataId, dataset):
        filename = butler.get(dataset + "_filename", dataId)[0]
        self.assertTrue("%s exists on disk" % dataset, os.path.exists(filename))
        self.assertGreater("%s has non-zero size" % dataset, os.stat(filename).st_size, 0)

    def validateSources(self, butler, dataId):
        src = butler.get(self._sourceDataset, dataId)
        self.assertGreater("Number of sources", len(src), self._minSources)

    def validateMatches(self, butler, dataId):
        # XXX lsst.meas.astrom.readMatches is gone!
        return
        matches = measAstrom.readMatches(butler, dataId,)
        self.assertGreater("Number of matches", len(matches), self._minMatches)

    def run(self, butler, dataId, **kwargs):
        if kwargs:
            dataId = dataId.copy()
            dataId.update(kwargs)

        for ds in self._datasets:
            self.log.write("*** Validating dataset %s for %s\n" % (ds, dataId))
            self.validateDataset(butler, dataId, ds)

        for f in self._files:
            self.log.write("*** Validating file %s for %s\n" % (f, dataId))
            self.validateFile(butler, dataId, f)

        if self._sourceDataset is not None:
            self.log.write("*** Validating source output for %s\n" % dataId)
            self.validateSources(butler, dataId)

        if self._matchDataset is not None:
            self.log.write("*** Validating matches output for %s\n" % dataId)
            self.validateMatches(butler, dataId)


class RawValidation(Validation):
    _datasets = ["raw"]

class DetrendValidation(Validation):
    _datasets = ["bias", "dark", "flat"]

class SfmValidation(Validation):
    _datasets = ["processCcd_config", "processCcd_metadata", "calexp", "calexpBackground",
                 "icSrc", "icSrc_schema", "src_schema"]
    _sourceDataset = "src"
    _matchDatasets = ["icMatch", "srcMatch"]
    _files=["ossThumb", "flattenedThumb", "plotMagHist", "plotSeeingRough",
            "plotSeeingRobust", "plotSeeingMap", "plotEllipseMap", "plotEllipticityMap",
            "plotFwhmGrid", "plotEllipseGrid", "plotEllipticityGrid"]

class SkymapValidation(Validation):
    _datasets = ["deepCoadd_skyMap"]

class WarpValidation(Validation):
    _datasets = ["deepCoadd_tempExp", "deep_makeCoaddTempExp_config", "deep_makeCoaddTempExp_metadata"]

class CoaddValidation(Validation):
    _datasets = ["deepCoadd", "deep_assembleCoadd_config", "deep_assembleCoadd_metadata"]

class DetectionValidation(Validation):
    _datasets = ["deepCoadd_det_schema", "detectCoaddSources_config", "detectCoaddSources_metadata"]
    _sourceDataset = "deepCoadd_det"

class MergeDetectionsValidation(Validation):
    _datasets = ["mergeCoaddDetections_config", "mergeCoaddDetections_metadata", "deepCoadd_mergeDet_schema"]
    _sourceDataset = "deepCoadd_mergeDet"

class MeasureValidation(Validation):
    _datasets = ["measureCoaddSources_config", "measureCoaddSources_metadata", "deepCoadd_meas_schema"]
    _sourceDataset = "deepCoadd_meas"
    _matchDataset = "deepCoadd_srcMatch"

class MergeMeasurementsValidation(Validation):
    _datasets = ["mergeCoaddMeasurements_config", "mergeCoaddMeasurements_metadata", "deepCoadd_ref_schema"]
    _sourceDataset = "deepCoadd_ref"

class ForcedValidation(Validation):
    _datasets = ["deepCoadd_forced_src_schema", "deepCoadd_forced_config", "deepCoadd_forced_metadata"]
    _sourceDataset = "deepCoadd_forced_src"
