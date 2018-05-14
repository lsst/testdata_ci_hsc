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
from lsst.daf.butler.core import Registry, Datastore, Config, StorageClassFactory
from lsst.daf.butler.gen2convert import ConversionWalker, ConversionWriter
from lsst.obs.subaru.gen3 import HyperSuprimeCam
from lsst.obs.hsc import HscMapper

REPO_ROOT = os.path.join(getPackageDir("ci_hsc"), "DATA")

butlerConfig = Config()
butlerConfig["registry.cls"] = "lsst.daf.butler.registries.sqliteRegistry.SqliteRegistry"
butlerConfig["registry.db"] = "sqlite:///{}/gen3.sqlite3".format(REPO_ROOT)
butlerConfig["registry.schema"] = os.path.join(getPackageDir("daf_butler"),
                                               "config/registry/default_schema.yaml")
butlerConfig["storageClasses.config"] = os.path.join(getPackageDir("daf_butler"),
                                                     "config/registry/storageClasses.yaml")
butlerConfig["datastore.cls"] = "lsst.daf.butler.datastores.posixDatastore.PosixDatastore"
butlerConfig["datastore.root"] = REPO_ROOT
butlerConfig["datastore.create"] = True
butlerConfig["datastore.records.table"] = "PosixDatastoreRecords"
butlerConfig["datastore.formatters"] = {
    "Catalog": "lsst.daf.butler.formatters.fitsCatalogFormatter.FitsCatalogFormatter",
    "PeakCatalog": "lsst.daf.butler.formatters.fitsCatalogFormatter.FitsCatalogFormatter",
    "SourceCatalog": "lsst.daf.butler.formatters.fitsCatalogFormatter.FitsCatalogFormatter",
    "ImageF": "lsst.daf.butler.formatters.fitsExposureFormatter.FitsExposureFormatter",
    "ImageU": "lsst.daf.butler.formatters.fitsExposureFormatter.FitsExposureFormatter",
    "DecoratedImageU": "lsst.daf.butler.formatters.fitsExposureFormatter.FitsExposureFormatter",
    "MaskX": "lsst.daf.butler.formatters.fitsExposureFormatter.FitsExposureFormatter",
    "Exposure": "lsst.daf.butler.formatters.fitsExposureFormatter.FitsExposureFormatter",
    "ExposureF": "lsst.daf.butler.formatters.fitsExposureFormatter.FitsExposureFormatter",
    "ExposureI": "lsst.daf.butler.formatters.fitsExposureFormatter.FitsExposureFormatter",
    "SkyMap": "lsst.daf.butler.formatters.pickleFormatter.PickleFormatter",
    "TablePersistableTransmissionCurve":
        "lsst.daf.butler.formatters.fitsCatalogFormatter.FitsCatalogFormatter",
    "Background": "lsst.daf.butler.formatters.fitsCatalogFormatter.FitsCatalogFormatter",
    "Config": "lsst.daf.butler.formatters.pexConfigFormatter.PexConfigFormatter",
    "Packages": "lsst.daf.butler.formatters.pickleFormatter.PickleFormatter",
}

StorageClassFactory.fromConfig(butlerConfig)

converterConfig = Config(os.path.join(getPackageDir("daf_butler"), "config/gen2convert.yaml"))
converterConfig["skymaps"] = {os.path.join(REPO_ROOT, "rerun", "ci_hsc"): "ci_hsc"}


def getRegistry():
    return Registry.fromConfig(butlerConfig)


def getDatastore(registry):
    return Datastore.fromConfig(config=butlerConfig, registry=registry)


def registerInstrument(registry):
    mapper = HscMapper(root=REPO_ROOT)
    instrument = HyperSuprimeCam(mapper)
    instrument.register(registry)


def walk():
    walker = ConversionWalker(converterConfig)
    walker.tryRoot(REPO_ROOT)
    walker.scanAll()
    return walker


def write(walker, registry, datastore):
    writer = ConversionWriter.fromWalker(walker)
    writer.run(registry, datastore)
