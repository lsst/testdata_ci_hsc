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

gen3validateCmds = {}

def validate(cls, root, dataId=None, gen3id=None, **kwargs):
    """!Construct a command-line for validation

    @param cls  Validation class to use
    @param root  Data repo root directory
    @param dataId  Data identifier dict (Gen2), or None
    @param gen3Id  Gen3 data identifier dict, or None
    @param kwargs  Additional key/value pairs to add to dataId
    @return Command-line string to run validation
    """
    if dataId:
        dataId = dataId.copy()
        dataId.update(kwargs)
    elif kwargs:
        dataId = kwargs
    cmd = [getExecutable("ci_hsc", "validate.py"), cls.__name__, root,]
    gen3 = cmd + ["--gen3", "--collection", "shared/ci_hsc"]
    if dataId:
        cmd += ["--id %s" % (" ".join("%s=%s" % (key, value) for key, value in dataId.items()))]
    if gen3id:
        gen3 += ["--id %s" % (" ".join("%s=%s" % (key, value) for key, value in gen3id.items()))]
        gen3validateCmds.setdefault(cls.__name__, []).append(" ".join(gen3))
    return " ".join(cmd)


profileNum = -1
def getProfiling(script):
    """Return python command-line argument string for profiling

    If activated (via the "--enable-profile" command-line argument),
    we write the profile to a filename starting with the provided
    base name and including a sequence number and the script name,
    so its contents can be quickly identified.

    Note that this is python function-level profiling, which won't
    descend into C++ elements of the codebase.

    A basic profile can be printed using python:

        >>> from pstats import Stats
        >>> stats = Stats("profile-123-script.pstats")
        >>> stats.sort_stats("cumulative").print_stats(30)
    """
    base = GetOption("enable_profile")
    if not base:
        return ""
    global profileNum
    profileNum += 1
    if script.endswith(".py"):
        script = script[:script.rfind(".")]
    return "-m cProfile -o %s-%03d-%s.pstats" % (base, profileNum, script)


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
    return "{} python {} {}".format(libraryLoaderEnvironment(),
                                    getProfiling(script),
                                    os.path.join(getPackageDir(package), "bin", script))

Execute(Mkdir(".scons"))

root = Dir('.').srcnode().abspath
AddOption("--raw", default=os.path.join(root, "raw"), help="Path to raw data")
AddOption("--repo", default=os.path.join(root, "DATA"), help="Path for data repository")
AddOption("--calib", default=os.path.join(root, "CALIB"), help="Path for calib repository")
AddOption("--rerun", default="ci_hsc", help="Rerun name")
AddOption("--no-versions", dest="no_versions", default=False, action="store_true",
          help="Add --no-versions for LSST scripts")
AddOption("--enable-profile", nargs="?", const="profile", dest="enable_profile",
          help=("Profile base filename; output will be <basename>-<sequence#>-<script>.pstats; "
                "(Note: this option is for profiling the scripts, while --profile is for scons)"))

RAW = GetOption("raw")
REPO = GetOption("repo")
CALIB = GetOption("calib")
PROC = GetOption("repo") + " --rerun " + GetOption("rerun")  # Common processing arguments
DATADIR = os.path.join(GetOption("repo"), "rerun", GetOption("rerun"))
STDARGS = "--doraise" + (" --no-versions" if GetOption("no_versions") else "")


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

    def gen3id(self, raw=False):
        """Returns the Gen3 data ID for this data"""
        if raw:
            return dict(camera="HSC", exposure=self.visit, sensor=self.ccd)
        else:
            return dict(camera="HSC", visit=self.visit, sensor=self.ccd)

    def id(self, prefix="--id", tract=None):
        """Returns a suitable --id command-line string"""
        r = "%s visit=%d ccd=%d" % (prefix, self.visit, self.ccd)
        if tract is not None:
            r += " tract=%d" % tract
        return r

    def sfm(self, env):
        """Process this data through single frame measurement"""
        return command("sfm-" + self.name, ingestValidations + calibValidations + [preSfm, refcat],
                       [getExecutable("pipe_tasks", "processCcd.py") + " " + PROC + " " + self.id() + " " +
                        STDARGS, validate(SfmValidation, DATADIR, self.dataId, gen3id=self.gen3id())])

    def forced(self, env, tract):
        """Process this data through CCD-level forced photometry"""
        dataId = self.dataId.copy()
        dataId["tract"] = tract
        return command("forced-ccd-" + self.name, ingestValidations + calibValidations + [preForcedPhotCcd],
                       [getExecutable("meas_base", "forcedPhotCcd.py") + " " + PROC + " " +
                       self.id(tract=tract) + " " + STDARGS + " -C forcedPhotCcdConfig.py",
                       validate(ForcedPhotCcdValidation, DATADIR, dataId,
                                gen3id=dict(tract=0, skymap="ci_hsc", **self.gen3id()))])


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

calib = env.Command(os.path.join(REPO, "CALIB"), mapper,
                    ["rm -f " + os.path.join(REPO, "CALIB"),
                     "ln -s " + CALIB + " " + os.path.join(REPO, "CALIB")]
                     )
ingest = env.Command(os.path.join(REPO, "registry.sqlite3"), calib,
                     [getExecutable("pipe_tasks", "ingestImages.py") + " " + REPO + " " + RAW +
                     "/*.fits --mode=link " + "-c clobber=True register.ignore=True " + STDARGS]
                      )
ingestValidations = [command("ingestValidation-%(visit)d-%(ccd)d" % data.dataId, ingest,
                             validate(RawValidation, REPO, data.dataId, gen3id=data.gen3id(True))) for
                     data in sum(allData.values(), [])]
calibValidations = [command("calibValidation-%(visit)d-%(ccd)d" % data.dataId, ingest,
                            validate(DetrendValidation, REPO, data.dataId)) for
                    data in sum(allData.values(), [])]

refcatName = "ps1_pv3_3pi_20170110"
refcatPath = os.path.join(REPO, "ref_cats", refcatName)
refcat = env.Command(refcatPath, mapper,
                     ["rm -f " + refcatPath,  # Delete any existing, perhaps leftover from previous
                      "ln -s %s %s" % (os.path.join(root, refcatName), refcatPath)])

brightObjSource = os.path.join(root, "brightObjectMasks")
brightObjTarget = os.path.join(REPO, "deepCoadd", "BrightObjectMasks")
brightObj = env.Command(brightObjTarget, mapper,
                        ["rm -f " + brightObjTarget,  # Delete any existing
                         "mkdir -p " + os.path.dirname(brightObjTarget),
                         "ln -s %s %s" % (brightObjSource, brightObjTarget)])

# Add transmission curves to the repository.
transmissionCurvesTarget = os.path.join(REPO, "transmission")
transmissionCurves = env.Command(transmissionCurvesTarget, calib,
                                 [getExecutable("obs_subaru", "installTransmissionCurves.py") + " " + REPO])

# Create skymap
# This needs to be done early and in serial, so that the package versions produced by it aren't clobbered
# by other commands in-flight.
skymap = command("skymap", mapper,
                 [getExecutable("pipe_tasks", "makeSkyMap.py") + " " + PROC + " -C skymap.py " + STDARGS,
                  validate(SkymapValidation, DATADIR, gen3id=dict(skymap="ci_hsc"))])

# Single frame measurement
# preSfm step is a work-around for a race on schema/config/versions
preSfm = command("sfm", [skymap, transmissionCurvesTarget],
                 getExecutable("pipe_tasks", "processCcd.py") + " " + PROC + " " + STDARGS)
env.Depends(preSfm, refcat)
sfm = {(data.visit, data.ccd): data.sfm(env) for data in sum(allData.values(), [])}

# Sky correction
def processSkyCorr(dataList):
    """Generate sky corrections"""
    visitDataLists = defaultdict(list)
    for filterName in allData:
        for data in allData[filterName]:
            visitDataLists[data.visit].append(data)
    preSkyCorr = command("skyCorr", skymap,
                         getExecutable("pipe_drivers", "skyCorrection.py") + " " + PROC + " " + STDARGS +
                         " --batch-type=smp --cores=1")
    nameList = ("skyCorr-%d" % (vv,) for vv in visitDataLists)
    depList = ([sfm[(data.visit, data.ccd)] for data in visitDataLists[vv]] for vv in visitDataLists)
    cmdList = (getExecutable("pipe_drivers", "skyCorrection.py") + " " + PROC + " " + STDARGS +
               " --batch-type=none --id visit=%d --job=skyCorr-%d" % (vv, vv) for vv in visitDataLists)
    validateList = ([validate(SkyCorrValidation, DATADIR, data.dataId, gen3id=data.gen3id())
                    for data in visitDataLists[vv]] for vv in visitDataLists)
    return {vv: command(target=name, source=[preSkyCorr] + dep, cmd=[cmd] + val)
            for vv, name, dep, cmd, val in zip(visitDataLists, nameList, depList, cmdList, validateList)}


skyCorr = processSkyCorr(allData)

patchDataId = dict(tract=0, patch="5,4")
patchGen3id = dict(skymap="ci_hsc", tract=0, patch=69)
patchId = " ".join(("%s=%s" % (k,v) for k,v in patchDataId.items()))

# Coadd construction
# preWarp, preCoadd and preDetect steps are a work-around for a race on schema/config/versions
preWarp = command("warp", skymap,
                  getExecutable("pipe_tasks", "makeCoaddTempExp.py") + " " + PROC + " " + STDARGS +
                  " -c doApplyUberCal=False ")
preCoadd = command("coadd", [skymap, brightObj],
                   getExecutable("pipe_tasks", "assembleCoadd.py") + " --warpCompareCoadd  " +
                   PROC + " " + STDARGS)
preDetect = command("detect", skymap,
                    getExecutable("pipe_tasks", "detectCoaddSources.py") + " " + PROC + " " + STDARGS)
def processCoadds(filterName, dataList):
    """Generate coadds and run detection on them"""
    ident = "--id " + patchId + " filter=" + filterName
    exposures = defaultdict(list)
    for data in dataList:
        exposures[data.visit].append(data)
    warps = [command("warp-%d" % exp,
                     [skymap, preWarp] + [skyCorr[exp]],
                     [getExecutable("pipe_tasks", "makeCoaddTempExp.py") +  " " + PROC + " " + ident +
                      " " + " ".join(data.id("--selectId") for data in exposures[exp]) + " " + STDARGS +
                      " -c doApplyUberCal=False",
                      validate(WarpValidation, DATADIR, patchDataId, visit=exp, filter=filterName,
                               gen3id=dict(camera="HSC", visit=exp, **patchGen3id))
                      ]) for exp in exposures]
    coadd = command("coadd-" + filterName, warps + [preCoadd],
                    [getExecutable("pipe_tasks", "assembleCoadd.py") + " --warpCompareCoadd " + PROC +
                     " " + ident + " " + " ".join(data.id("--selectId") for data in dataList) + " " +
                     STDARGS,
                     validate(CoaddValidation, DATADIR, patchDataId, filter=filterName,
                              gen3id=dict(abstract_filter=filterName[-1].lower(), **patchGen3id))
                     ])
    detect = command("detect-" + filterName, [coadd, preDetect],
                     [getExecutable("pipe_tasks", "detectCoaddSources.py") + " " + PROC + " " + ident +
                      " " + STDARGS,
                      validate(DetectionValidation, DATADIR, patchDataId, filter=filterName,
                               gen3id=dict(abstract_filter=filterName[-1].lower(), **patchGen3id))
                      ])
    return detect

coadds = {ff: processCoadds(ff, allData[ff]) for ff in allData}

# Multiband processing
filterList = coadds.keys()
mergeDetections = command("mergeDetections", sum(coadds.values(), []),
                          [getExecutable("pipe_tasks", "mergeCoaddDetections.py") + " " + PROC + " --id " +
                           patchId + " filter=" + "^".join(filterList) + " " + STDARGS,
                           validate(MergeDetectionsValidation, DATADIR, patchDataId, gen3id=patchGen3id)
                           ])

# Since the deblender input is a single mergedDet catalog,
# but the output is a SourceCatalog in each band,
# we have to validate each band separately
deblendValidation = [validate(DeblendSourcesValidation, DATADIR, patchDataId, filter=ff) for ff in filterList]
deblendSources = command("deblendSources", mergeDetections,
                         [getExecutable("pipe_tasks", "deblendCoaddSources.py") + " " + PROC + " --id " +
                           patchId + " filter=" + "^".join(filterList) + " " + STDARGS
                         ] + deblendValidation)

# preMeasure step is a work-around for a race on schema/config/versions
preMeasure = command("measure", deblendSources,
                     getExecutable("pipe_tasks", "measureCoaddSources.py") + " " + PROC + " " + STDARGS)
def measureCoadds(filterName):
    return command("measure-" + filterName, preMeasure,
                   [getExecutable("pipe_tasks", "measureCoaddSources.py") + " " + PROC + " --id " +
                    patchId + " filter=" + filterName + " " + STDARGS,
                    validate(MeasureValidation, DATADIR, patchDataId, filter=filterName,
                             gen3id=dict(abstract_filter=filterName[-1].lower(), **patchGen3id))
                    ])

measure = [measureCoadds(ff) for ff in filterList]

mergeMeasurements = command("mergeMeasurements", measure,
                            [getExecutable("pipe_tasks", "mergeCoaddMeasurements.py") + " " + PROC +
                             " --id " + patchId + " filter=" + "^".join(filterList) + " " + STDARGS,
                             validate(MergeMeasurementsValidation, DATADIR, patchDataId, gen3id=patchGen3id)
                             ])

# preForcedPhotCoadd step is a work-around for a race on schema/config/versions
preForcedPhotCoadd = command("forcedPhotCoadd", [mapper, mergeMeasurements],
                             getExecutable("meas_base", "forcedPhotCoadd.py") + " " + PROC + " " + STDARGS)
def forcedPhotCoadd(filterName):
    return command("forced-coadd-" + filterName, [mergeMeasurements, preForcedPhotCoadd],
                   [getExecutable("meas_base", "forcedPhotCoadd.py") + " " + PROC + " --id " + patchId +
                    " filter=" + filterName + " " + STDARGS,
                    validate(ForcedPhotCoaddValidation, DATADIR, patchDataId, filter=filterName,
                             gen3id=dict(abstract_filter=filterName[-1].lower(), **patchGen3id))
                    ])

forcedPhotCoadd = [forcedPhotCoadd(ff) for ff in filterList]

# preForcedPhotCcd step is a work-around for a race on schema/config/versions
preForcedPhotCcd = command("forcedPhotCcd", [mapper, mergeMeasurements],
                           getExecutable("meas_base", "forcedPhotCcd.py") + " " + PROC +
                           " -C forcedPhotCcdConfig.py" + " " + STDARGS)

forcedPhotCcd = [data.forced(env, tract=0) for data in sum(allData.values(), [])]

gen3repo = env.Command(os.path.join(REPO, "gen3.sqlite3"), [forcedPhotCcd, forcedPhotCoadd],
                       [getExecutable("ci_hsc", "gen3.py")])
env.Alias("gen3repo", gen3repo)

gen3repoValidate = [command("gen3repo-{}".format(k), [gen3repo], v) for k, v in gen3validateCmds.items()]
env.Alias("gen3repo-validate", gen3repoValidate)

everything = [gen3repoValidate]

if not GetOption("no_versions"):
    versions = command("versions", [forcedPhotCcd, forcedPhotCoadd], validate(VersionValidation, DATADIR, {}))
    everything.append(versions)

# Add a no-op install target to keep Jenkins happy.
env.Alias("install", "SConstruct")

env.Alias("all", everything)
Default(everything)

env.Clean(everything, [".scons", "DATA/rerun/ci_hsc"])
