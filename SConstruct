# -*- python -*-

import os
from collections import defaultdict
from lsst.pipe.base import Struct

env = Environment(ENV=os.environ)
Execute(Mkdir(".scons"))

root = Dir('.').srcnode().abspath
AddOption("--raw", default=os.path.join(root, "raw"), help="Path to raw data")
AddOption("--repo", default=os.path.join(root, "DATA"), help="Path for data repository")
AddOption("--calib", default=os.path.join(root, "CALIB"), help="Path for calib repository")

RAW = GetOption("raw")
REPO = GetOption("repo")
CALIB = GetOption("calib")


def getButler():
    try:
        return getButler._butler
    except NameError:
        from lsst.daf.persistence import Butler
        getButler._butler = Butler(REPO)
    return getButler._butler

def command(target, source, cmd):
    name = os.path.join(".scons", target)
    if isinstance(cmd, str):
        cmd = [cmd]
    out = env.Command(name, source, cmd + [Touch(name)])
    env.Alias(target, name)
    return out

class Data(Struct):
    def __init__(self, visit, ccd):
        Struct.__init__(self, visit=visit, ccd=ccd)

    @property
    def name(self):
        return "%d-%d" % (self.visit, self.ccd)

    @property
    def dataId(self):
        return dict(visit=self.visit, ccd=self.ccd)

    def id(self, prefix="--id"):
        return "%s visit=%d ccd=%d" % (prefix, self.visit, self.ccd)

    def sfm(self, env):
        return command("sfm-" + self.name, [ingest, calib],
                       "processCcd.py " + REPO + " " + self.id() + " --doraise")

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

mapper = env.Command(os.path.join(REPO, "_mapper"), [],
                     ["mkdir -p " + REPO,
                      "echo lsst.obs.hsc.HscMapper > " + os.path.join(REPO, "_mapper"),
                      ])
rawValid = validation.RawValidation()
ingest = env.Command(os.path.join(REPO, "registry.sqlite3"), mapper,
                     ["ingestImages.py " + REPO + " " + RAW + "/*.fits --mode=link " +
                      "-c clobber=True register.ignore=True --doraise"] +
                     [rawValid.run(getButler(), data.dataId) for data in sum(allData.itervalues(), [])])
calib = env.Command(os.path.join(REPO, "CALIB"), mapper,
                    ["rm -f " + os.path.join(REPO, "CALIB"),
                     "ln -s " + CALIB + " " + os.path.join(REPO, "CALIB"),
                     validation.DetrendValidation().run(getButler(), data.dataId) for
                     data in sum(allData.itervalues(), [])
                     ])

sfm = {(data.visit, data.ccd): data.sfm(env) for data in sum(allData.itervalues(), [])}

skymap = command("skymap", mapper,
                 ["makeSkyMap.py " + REPO + " -C skymap.py --doraise",
                  validation.SkymapValidation().run(getButler(), {}),
                 ])

patchDataId = dict(tract=0, patch="5,4")
patchId = " ".join("%s=%s" % k,v for k,v in patchDataId.iteritems())

def processCoadds(filterName, dataList):
    ident = "--id " + patchId + " filter=" + filterName
    exposures = defaultdict(list)
    for data in dataList:
        exposures[data.visit].append(data)
    warpValid = validation.WarpValidation()
    warps = [command("warp-%d" % exp, [sfm[(data.visit, data.ccd)] for data in exposures[exp]] + [skymap],
                     ["makeCoaddTempExp.py " + REPO + " " + ident +
                      " " + " ".join(data.id("--selectId") for data in exposures[exp]) + " --doraise",
                      warpValid.run(getButler(), patchDataId, visit=exp)]) for exp in exposures]
    coaddValid = validation.CoaddValidation()
    coadd = command("coadd-" + filterName, warps,
                    ["assembleCoadd.py " + REPO + " " + ident + " " +
                     " ".join(data.id("--selectId") for data in dataList) + " --doraise",
                     coaddValid.run(getButler(), patchDataId, filter=filterName)
                     ])
    detect = command("detect-" + filterName, coadd,
                     ["detectCoaddSources.py " + REPO + " " + ident + " --doraise",
                      validation.DetectionValidation().run(getButler(), patchDataId, filter=filterName)
                      ])
    return detect

coadds = {ff: processCoadds(ff, allData[ff]) for ff in allData}
filterList = coadds.keys()
mergeDetections = command("mergeDetections", sum(coadds.itervalues(), []),
                          ["mergeCoaddDetections.py " + REPO + " --id " + patchId + " filter=" +
                           "^".join(filterList) + " --doraise",
                           validation.MergeDetectionsValidation().run(getButler(), patchDataId),
                           ])

def measureCoadds(filterName):
    return command("measure-" + filterName, mergeDetections,
                   ["measureCoaddSources.py " + REPO + " --id " + patchId + " filter=" + filterName +
                    " --doraise",
                    validation.MeasureValidation().run(getButler(), patchDataId, filter=filterName),
                    ])

measure = [measureCoadds(ff) for ff in filterList]

mergeMeasurements = command("mergeMeasurements", measure,
                            ["mergeCoaddMeasurements.py " + REPO + " --id " + patchId +
                             " filter=" + "^".join(filterList) + " --doraise",
                             validation.MergeMeasurementsValidation().run(getButler(), patchDataId),
                             ])

def forcedPhot(filterName):
    return command("forced-" + filterName, mergeMeasurements,
                   ["forcedPhotCoadd.py " + REPO + " --id " + patchId + " filter=" + filterName +
                    " --doraise",
                    validation.ForcedValidation().run(getButler(), patchDataID, filter=filterName),
                    ])

forced = [forcedPhot(ff) for ff in filterList]

env.Alias("all", forced)
Default(forced)
