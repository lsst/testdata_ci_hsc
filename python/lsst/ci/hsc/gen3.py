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

__all__ = ("Gen3ButlerWrapper", "walk", "write")

import os

from lsst.utils import getPackageDir
from lsst.daf.butler import Butler, ButlerConfig, Registry, Datastore, Config, StorageClassFactory
from lsst.daf.butler.gen2convert import ConversionWalker, ConversionWriter

REPO_ROOT = os.path.join(getPackageDir("ci_hsc"), "DATA")

converterConfig = Config(os.path.join(getPackageDir("daf_butler"), "config/gen2convert.yaml"))
converterConfig["skymaps"] = {"ci_hsc": os.path.join(REPO_ROOT, "rerun", "ci_hsc")}
converterConfig["regions"][0]["collection"] = "shared/ci_hsc"

searchPaths = [os.path.join(getPackageDir("ci_hsc"), "gen3config"), ]


class Gen3ButlerWrapper:
    """A class to simplify access to a gen 3 `~lsst.daf.butler.Butler`.

    Parameters
    ----------
    config : `~lsst.daf.butler.Config` or `str`, optional
        Something that can be passed to a `~lsst.daf.butler.ButlerConfig`
        constructor.  If `None` the configuration will be read from the
        value of the ``root`` parameter.
    root : `str`, optional
        Root directory of the butler repository to use.  Defaults to
        the ``DATA`` directory in the ``ci_hsc`` package.
    """

    def __init__(self, config=None, root=REPO_ROOT):

        self.root = root
        if config is None:
            config = self.root
        self.butlerConfig = ButlerConfig(config, searchPaths=searchPaths)
        StorageClassFactory().addFromConfig(self.butlerConfig)

        # Force the configuration directory to refer to the ci_hsc root
        self.butlerConfig.configDir = self.root

    def getRegistry(self):
        return Registry.fromConfig(self.butlerConfig, butlerRoot=self.root)

    def getDatastore(self, registry):
        return Datastore.fromConfig(config=self.butlerConfig, registry=registry, butlerRoot=self.root)

    def getButler(self, collection):
        return Butler(config=self.butlerConfig, run=collection)


def walk():
    walker = ConversionWalker(converterConfig)
    walker.tryRoot(REPO_ROOT)
    walker.scanAll()
    walker.readObsInfo()
    return walker


def write(walker, registry, datastore):
    writer = ConversionWriter.fromWalker(walker)
    writer.run(registry, datastore)
