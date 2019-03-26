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

from lsst.utils import getPackageDir
from lsst.daf.butler import Butler, ButlerConfig, Registry, Datastore, Config, StorageClassFactory
from lsst.daf.butler.gen2convert import ConversionWalker, ConversionWriter

REPO_ROOT = os.path.join(getPackageDir("ci_hsc"), "DATA")

converterConfig = Config(os.path.join(getPackageDir("daf_butler"), "config/gen2convert.yaml"))
converterConfig["skymaps"] = {"ci_hsc": os.path.join(REPO_ROOT, "rerun", "ci_hsc")}
converterConfig["regions"][0]["collection"] = "shared/ci_hsc"

butlerConfig = ButlerConfig(REPO_ROOT)
StorageClassFactory().addFromConfig(butlerConfig)


def getRegistry():
    return Registry.fromConfig(butlerConfig, butlerRoot=REPO_ROOT)


def getDatastore(registry):
    return Datastore.fromConfig(config=butlerConfig, registry=registry, butlerRoot=REPO_ROOT)


def getButler(collection):
    return Butler(config=butlerConfig, run=collection)


def walk():
    walker = ConversionWalker(converterConfig)
    walker.tryRoot(REPO_ROOT)
    walker.scanAll()
    walker.readObsInfo()
    return walker


def write(walker, registry, datastore):
    writer = ConversionWriter.fromWalker(walker)
    writer.run(registry, datastore)
