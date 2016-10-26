# -*- python -*-

import os
import functools
from collections import defaultdict
from lsst.pipe.base import Struct
from lsst.sconsUtils.utils import libraryLoaderEnvironment
from lsst.utils import getPackageDir
from lsst.ci.hsc.validate import *

from SCons.Script import SConscript
SConscript(os.path.join(".", "bin.src", "SConscript"))  # build bin scripts

env = Environment(ENV=os.environ)
env["ENV"]["OMP_NUM_THREADS"] = "1"  # Disable threading; we're parallelising at a higher level

def validate(cls, root, dataId=None, **kwargs):
    """!Construct a command-line for validation

    @param cls  Validation class to use
    @param root  Data repo root directory
    @param dataId  Data identifier dict, or None
    @param kwargs  Additional key/value pairs to add to dataId
    @return Command-line string to run validation
    """
    if dataId:
        dataId = dataId.copy()
        dataId.update(kwargs)
    else:
        assert len(kwargs) == 0  # There's no dataId to update
    cmd = [getExecutable("ci_hsc", "validate.py"), cls.__name__, root,]
    if dataId:
        cmd += ["--id %s" % (" ".join("%s=%s" % (key, value) for key, value in dataId.iteritems()))]
    return " ".join(cmd)

def getExecutable(package, script):
    """
    Given the name of a package and a script or other executable which lies
    within its `bin` subdirectory, return an appropriate string which can be
    used to set up an appropriate environment and execute the command.

    This includes:
    * Specifying an explict list of paths to be searched by the dynamic linker;
    * Specifying a Python executable to be run (we assume the one on the default ${PATH} is appropriate);
    * Specifying the complete path to the script.
    """
    return "{} python {}".format(libraryLoaderEnvironment(),
                                 os.path.join(getPackageDir(package), "bin", script))

Execute(Mkdir(".scons"))

root = Dir('.').srcnode().abspath
AddOption("--raw", default=os.path.join(root, "raw"), help="Path to raw data")
AddOption("--repo", default=os.path.join(root, "DATA"), help="Path for data repository")
AddOption("--calib", default=os.path.join(root, "CALIB"), help="Path for calib repository")
AddOption("--rerun", default="ci_hsc", help="Rerun name")

RAW = GetOption("raw")
REPO = GetOption("repo")
CALIB = GetOption("calib")
PROC = GetOption("repo") + " --rerun " + GetOption("rerun")  # Common processing arguments
DATADIR = os.path.join(GetOption("repo"), "rerun", GetOption("rerun"))


def command(target, source, cmd):
    """Run a command and record that we ran it

    The record is in the form of a file in the ".scons" directory.
    """
    name = os.path.join(".scons", target)
    if isinstance(cmd, str):
        cmd = [cmd]
    out = env.Command(name, source, cmd + [Touch(name)])
    env.Alias(target, name)
    return out

class Data(Struct):
    """Data we can process"""
    def __init__(self, visit, ccd):
        Struct.__init__(self, visit=visit, ccd=ccd)

    @property
    def name(self):
        """Returns a suitable name for this data"""
        return "%d-%d" % (self.visit, self.ccd)

    @property
    def dataId(self):
        """Returns the dataId for this data"""
        return dict(visit=self.visit, ccd=self.ccd)

    def id(self, prefix="--id"):
        """Returns a suitable --id command-line string"""
        return "%s visit=%d ccd=%d" % (prefix, self.visit, self.ccd)

    def sfm(self, env):
        """Process this data through single frame measurement"""
        return command("sfm-" + self.name, ingestValidations + calibValidations + [preSfm],
                       [getExecutable("pipe_tasks", "processCcd.py") + " " + PROC + " " + self.id() +
                        " --doraise -c charImage.installSimplePsf.fwhm=4 ", validate(SfmValidation, DATADIR, self.dataId)])

allData = {"HSC-R": [Data(903334, 16),
                     Data(903334, 22),
                     Data(903334, 23),
                     Data(903334, 100),
                     Data(903336, 17),
                     Data(903336, 24),
                     Data(903338, 18),
                     Data(903338, 25),
                     Data(903342, 4),
                     Data(903342, 10),
                     Data(903342, 100),
                     Data(903344, 0),
                     Data(903344, 5),
                     Data(903344, 11),
                     Data(903346, 1),
                     Data(903346, 6),
                     Data(903346, 12),
                     ],
           "HSC-I": [Data(903986, 16),
                     Data(903986, 22),
                     Data(903986, 23),
                     Data(903986, 100),
                     Data(904014, 1),
                     Data(904014, 6),
                     Data(904014, 12),
                     Data(903990, 18),
                     Data(903990, 25),
                     Data(904010, 4),
                     Data(904010, 10),
                     Data(904010, 100),
                     Data(903988, 16),
                     Data(903988, 17),
                     Data(903988, 23),
                     Data(903988, 24),
                     ],
          }

# Set up the data repository
mapper = env.Command(os.path.join(REPO, "_mapper"), ["bin"],
                     ["mkdir -p " + REPO,
                      "echo lsst.obs.hsc.HscMapper > " + os.path.join(REPO, "_mapper"),
                      ])

ingest = env.Command(os.path.join(REPO, "registry.sqlite3"), mapper,
                     [getExecutable("pipe_tasks", "ingestImages.py") + " " + REPO + " " + RAW +
                      "/*.fits --mode=link " + "-c clobber=True register.ignore=True --doraise"]
                      )
calib = env.Command(os.path.join(REPO, "CALIB"), ingest,
                    ["rm -f " + os.path.join(REPO, "CALIB"),
                     "ln -s " + CALIB + " " + os.path.join(REPO, "CALIB")]
                     )
ingestValidations = [command("ingestValidation-%(visit)d-%(ccd)d" % data.dataId, ingest,
                             validate(RawValidation, REPO, data.dataId)) for
                     data in sum(allData.itervalues(), [])]
calibValidations = [command("calibValidation-%(visit)d-%(ccd)d" % data.dataId, calib,
                            validate(DetrendValidation, REPO, data.dataId)) for
                    data in sum(allData.itervalues(), [])]

# Single frame measurement
# preSfm step is a work-around for a race on schema/config/versions
preSfm = command("sfm", mapper, getExecutable("pipe_tasks", "processCcd.py") + " " + PROC + " --doraise"\
                 " -c charImage.installSimplePsf.fwhm=4 ")
sfm = {(data.visit, data.ccd): data.sfm(env) for data in sum(allData.itervalues(), [])}

# Create skymap
skymap = command("skymap", mapper,
                 [getExecutable("pipe_tasks", "makeSkyMap.py") + " " + PROC + " -C skymap.py --doraise",
                  validate(SkymapValidation, DATADIR)])

patchDataId = dict(tract=0, patch="5,4")
patchId = " ".join(("%s=%s" % (k,v) for k,v in patchDataId.iteritems()))


# Coadd construction
# preWarp, preCoadd and preDetect steps are a work-around for a race on schema/config/versions
preWarp = command("warp", mapper,
                  getExecutable("pipe_tasks", "makeCoaddTempExp.py") + " " + PROC + " --doraise"\
                  " -c doApplyUberCal=False ")
preCoadd = command("coadd", mapper,
                   getExecutable("pipe_tasks", "assembleCoadd.py") + " " + PROC + " --doraise")
preDetect = command("detect", mapper,
                    getExecutable("pipe_tasks", "detectCoaddSources.py") + " " + PROC + " --doraise")
def processCoadds(filterName, dataList):
    """Generate coadds and run detection on them"""
    ident = "--id " + patchId + " filter=" + filterName
    exposures = defaultdict(list)
    for data in dataList:
        exposures[data.visit].append(data)
    warps = [command("warp-%d" % exp,
                     [sfm[(data.visit, data.ccd)] for data in exposures[exp]] + [skymap, preWarp],
                     [getExecutable("pipe_tasks", "makeCoaddTempExp.py") +  " " + PROC + " " + ident +
                      " " + " ".join(data.id("--selectId") for data in exposures[exp]) + " --doraise"\
                      " -c doApplyUberCal=False ",
                      validate(WarpValidation, DATADIR, patchDataId, visit=exp, filter=filterName)]) for
             exp in exposures]
    coadd = command("coadd-" + filterName, warps + [preCoadd],
                    [getExecutable("pipe_tasks", "assembleCoadd.py") + " " + PROC + " " + ident + " " +
                     " ".join(data.id("--selectId") for data in dataList) + " --doraise",
                     validate(CoaddValidation, DATADIR, patchDataId, filter=filterName)
                     ])
    detect = command("detect-" + filterName, [coadd, preDetect],
                     [getExecutable("pipe_tasks", "detectCoaddSources.py") + " " + PROC + " " + ident +
                      " --doraise", validate(DetectionValidation, DATADIR, patchDataId, filter=filterName)
                      ])
    return detect

coadds = {ff: processCoadds(ff, allData[ff]) for ff in allData}

# Multiband processing
filterList = coadds.keys()
mergeDetections = command("mergeDetections", sum(coadds.itervalues(), []),
                          [getExecutable("pipe_tasks", "mergeCoaddDetections.py") + " " + PROC + " --id " +
                           patchId + " filter=" + "^".join(filterList) + " --doraise",
                           validate(MergeDetectionsValidation, DATADIR, patchDataId)
                           ])

# preMeasure step is a work-around for a race on schema/config/versions
preMeasure = command("measure", mergeDetections,
                     getExecutable("pipe_tasks", "measureCoaddSources.py") + " " + PROC + " --doraise")
def measureCoadds(filterName):
    return command("measure-" + filterName, preMeasure,
                   [getExecutable("pipe_tasks", "measureCoaddSources.py") + " " + PROC + " --id " +
                    patchId + " filter=" + filterName + " --doraise",
                    validate(MeasureValidation, DATADIR, patchDataId, filter=filterName)
                    ])

measure = [measureCoadds(ff) for ff in filterList]

mergeMeasurements = command("mergeMeasurements", measure,
                            [getExecutable("pipe_tasks", "mergeCoaddMeasurements.py") + " " + PROC +
                             " --id " + patchId + " filter=" + "^".join(filterList) + " --doraise",
                             validate(MergeMeasurementsValidation, DATADIR, patchDataId)
                             ])

# preForced step is a work-around for a race on schema/config/versions
preForced = command("forced", [mapper, mergeMeasurements],
                    getExecutable("meas_base", "forcedPhotCoadd.py") + " " + PROC + " --doraise")
def forcedPhot(filterName):
    return command("forced-" + filterName, [mergeMeasurements, preForced],
                   [getExecutable("meas_base", "forcedPhotCoadd.py") + " " + PROC + " --id " + patchId +
                    " filter=" + filterName + " --doraise",
                    validate(ForcedValidation, DATADIR, patchDataId, filter=filterName)
                    ])

forced = [forcedPhot(ff) for ff in filterList]

# Add a no-op install target to keep Jenkins happy.
env.Alias("install", "SConstruct")

env.Alias("all", forced)
Default(forced)

env.Clean(forced, [".scons", "DATA/rerun/ci_hsc"])
