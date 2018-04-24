# This file is part of ci_hsc.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

from lsst.log import Log
from lsst.utils import getPackageDir
from lsst.daf.butler.core import Registry, Config, StorageClassFactory
from lsst.daf.butler.gen2convert import ConversionWalker, ConversionWriter
from lsst.obs.subaru.gen3 import HyperSuprimeCam
from lsst.obs.hsc import HscMapper

REPO_ROOT = os.path.join(getPackageDir("ci_hsc"), "DATA")


log = Log.getLogger("lsst.daf.butler.gen2convert")
log.setLevel(Log.DEBUG)


def getRegistry():
    config = Config()
    config["registry.cls"] = "lsst.daf.butler.registries.sqliteRegistry.SqliteRegistry"
    config["registry.db"] = "sqlite:///{}/gen3.sqlite3".format(REPO_ROOT)
    config["registry.schema"] = os.path.join(getPackageDir("daf_butler"),
                                             "config/registry/default_schema.yaml")
    config["storageClasses.config"] = os.path.join(getPackageDir("daf_butler"),
                                                   "config/registry/storageClasses.yaml")
    StorageClassFactory.fromConfig(config)
    return Registry.fromConfig(config)


def registerInstrument(registry):
    mapper = HscMapper(root=REPO_ROOT)
    instrument = HyperSuprimeCam(mapper)
    instrument.register(registry)


def walk():
    config = Config(os.path.join(getPackageDir("daf_butler"), "config/gen2convert.yaml"))
    walker = ConversionWalker(config)
    walker.tryRoot(REPO_ROOT)
    while walker.found.keys() != walker.scanned.keys():
        repos = walker.found.copy()
        while repos:
            walker.scanRepo(repos.popitem()[1])
    walker.readVisitInfo()
    return walker


def write(walker, registry):
    config = Config(os.path.join(getPackageDir("daf_butler"), "config/gen2convert.yaml"))
    config["skymaps"] = {os.path.join(REPO_ROOT, "rerun", "ci_hsc"): "ci_hsc"}
    writer = ConversionWriter(config, gen2repos=walker.scanned, skyMaps=walker.skyMaps,
                              visitInfo=walker.visitInfo)
    writer.run(registry, None)
