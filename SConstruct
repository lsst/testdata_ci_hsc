# -*- python -*-

import os
from collections import defaultdict
from lsst.pipe.base import Struct

env = Environment(ENV=os.environ)

root = Dir('.').srcnode().abspath
AddOption("--raw", default=os.path.join(root, "raw"), help="Path to raw data")
AddOption("--repo", default=os.path.join(root, "DATA"), help="Path for data repository")

RAW = GetOption("raw")
REPO = GetOption("repo")


def verify():
    return
#    return env.Command(name, dep, "verifyFooBar.py ...")

class Data(Struct):
    def __init__(self, visit, ccd):
        Struct.__init__(self, visit=visit, ccd=ccd)
        self._sfm = None

    @property
    def name(self):
        return "%d-%d" % (self.visit, self.ccd)

    def id(self, prefix="--id"):
        return "%s visit=%d ccd=%d" % (prefix, self.visit, self.ccd)

    def sfm(self, env):
        if not self._sfm:
            self._sfm = env.Command("runSfm-" + self.name, ingest,
                                    "processCcd.py " + REPO + " " + self.id())
            verify()
        return self._sfm

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

mkdir = env.Command("mkdir", [], "mkdir -p " + REPO)
mapper = env.Command("mapper", mkdir,
                     "echo lsst.obs.hsc.HscMapper > " + os.path.join(REPO, "_mapper"))
ingest = env.Command(os.path.join(REPO, "registry.sqlite3"), [mapper, RAW],
                     "ingestImages.py " + REPO + " " + RAW + "/*.fits --mode=link")
verify()

sfm = {(data.visit, data.ccd): data.sfm(env) for data in sum(allData.itervalues(), [])}

skymap = env.Command("skymap", mapper, "makeSkyMap.py " + REPO + " -c skymap.py")
verify()

patchId = "tract=0 patch=5,4"

def processCoadds(filterName, dataList):
    ident = "--id " + patchId + " filter=" + filterName
    exposures = defaultdict(list)
    for data in dataList:
        exposures[data.visit].append(data)
    warps = [env.Command("warp-%d" % exp, [sfm[(data.visit, data.ccd)] for data in exposures[exp]] + [skymap],
                         "makeCoaddTempExp.py " + REPO + " " + ident +
                         " " + " ".join(data.id("--selectId") for data in exposures[exp]))
             for exp in exposures]
    verify()
    coadd = env.Command("coadd-" + filterName, warps,
                        "assembleCoadd.py " + REPO + " " + ident + " " +
                        " ".join(data.id("--selectId") for data in dataList))
    verify()
    detect = env.Command("detect-" + filterName, coadd,
                         "detectCoaddSources.py " + REPO + " " + ident)
    verify()
    return detect

coadds = {ff: processCoadds(ff, allData[ff]) for ff in allData}
filterList = coadds.keys()
mergeDetections = env.Command("mergeDetections", sum(coadds.itervalues(), []),
                              "mergeCoaddDetections.py " + REPO + " --id " + patchId + " filter=" +
                              "^".join(filterList))

def measureCoadds(filterName):
    measure = env.Command("measure-" + filterName, mergeDetections,
                          "measureCoaddSources.py " + REPO + " --id " + patchId + " filter=" + filterName)
    verify()
    return measure

measure = [measureCoadds(ff) for ff in filterList]

mergeMeasurements = env.Command("mergeMeasurements", measure,
                                "mergeCoaddMeasurements.py " + REPO + " --id " + patchId +
                                "filter=" + "^".join(filterList))

def forcedPhot(filterName):
    run = env.Command("forced-" + filterName, mergeMeasurements,
                      "forcedPhotCoadd.py " + REPO + " --id " + patchId + " filter=" + filterName)
    verify()
    return run

forced = [forcedPhot(ff) for ff in filterList]

env.Alias("all", forced)
Default(forced)
