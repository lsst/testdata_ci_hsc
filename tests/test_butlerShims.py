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
import unittest
from tempfile import TemporaryDirectory

import lsst.utils.tests
import lsst.afw.image.testUtils  # noqa; injects test methods into TestCase
from lsst.afw.table import SourceCatalog
from lsst.utils import getPackageDir
from lsst.daf.persistence import Butler as Butler2
from lsst.daf.butler import Butler as Butler3, DatasetType
from lsst.pipe.base.shims import ShimButler


REPO_ROOT = os.path.join(getPackageDir("ci_hsc"), "DATA")
TESTDIR = os.path.abspath(os.path.dirname(__file__))


class ButlerShimsTestCase(lsst.utils.tests.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.butler2 = Butler2(os.path.join(REPO_ROOT, "rerun", "ci_hsc"))
        cls.butler3 = Butler3(REPO_ROOT, run="shared/ci_hsc")
        cls.butlerShim = ShimButler(cls.butler3)

    @classmethod
    def tearDownClass(cls):
        del cls.butler2
        del cls.butler3
        del cls.butlerShim

    def setUp(self):
        # a valid exposure+detector data ID
        self.dataId2a = dict(visit=903334, ccd=16)
        self.dataId3a = dict(exposure=903334, detector=16, instrument="HSC")
        # a valid coadd data ID
        self.dataId2b = dict(tract=0, patch="5,4", filter="HSC-I")
        self.dataId3b = dict(tract=0, patch=69, abstract_filter="i", skymap="ci_hsc")
        # a visit+detector data ID that doesn't exist in this repo
        self.dataId2c = dict(visit=1000, ccd=12)
        self.dataId3c = dict(visit=1000, detector=12, instrument="HSC")

    def testDatasetExists(self):
        self.assertTrue(self.butler2.datasetExists("raw", self.dataId2a))
        self.assertTrue(self.butlerShim.datasetExists("raw", self.dataId3a))
        self.assertTrue(self.butler2.datasetExists("deepCoadd_meas", self.dataId2b))
        self.assertTrue(self.butlerShim.datasetExists("deepCoadd_meas", self.dataId3b))
        self.assertFalse(self.butler2.datasetExists("calexp", self.dataId2c))
        self.assertFalse(self.butlerShim.datasetExists("calexp", self.dataId3c))

    def assertDictSubsetsEqual(self, a, b, n=1):
        """Require a and b to have at least n keys in common, and that all keys
        in common have the same values.
        """
        intersection = a.keys() & b.keys()
        self.assertEqual({k: a[k] for k in intersection},
                         {k: b[k] for k in intersection})
        self.assertGreaterEqual(len(intersection), n)

    def testGetRaw(self):
        raw2 = self.butler2.get("raw", self.dataId2a)
        raw3 = self.butlerShim.get("raw", self.dataId3a)
        self.assertMaskedImagesEqual(raw2.maskedImage, raw3.maskedImage)

        md2FromRaw = raw2.getMetadata().toDict()
        md2Direct = self.butler2.get("raw_md", self.dataId2a).toDict()
        md3FromRaw = raw3.getMetadata().toDict()
        md3Direct = self.butlerShim.get("raw_md", self.dataId3a).toDict()
        # Gen2 isn't very careful about stripping metadata the same way in
        # different code paths, so we can only check that the keys that do
        # exist have the same values.
        self.assertDictSubsetsEqual(md2FromRaw, md2Direct)
        self.assertDictSubsetsEqual(md2FromRaw, md3FromRaw)
        # Gen3 is careful about this; metadata should be exactly the same.
        self.assertEqual(md3FromRaw, md3Direct)

        wcs2FromRaw = raw2.getWcs()
        wcs2Direct = self.butler2.get("raw_wcs", self.dataId2a)  # noqa
        wcs3FromRaw = raw3.getWcs()
        wcs3Direct = self.butlerShim.get("raw_wcs", self.dataId3a)
        # Gen2 is again not internally consistent about the WCS component;
        # I think the problem is that "raw_wcs" doesn't flip, but that's just
        # a guess.
        # Hence we don't test wcs2Direct.
        #
        # Gen3 is internally consistent and consistent with getting the Gen2
        # WCS from the full Exposure.
        self.assertEqual(wcs2FromRaw, wcs3FromRaw)
        self.assertEqual(wcs3FromRaw, wcs3Direct)

        visitInfo2FromRaw = raw2.getInfo().getVisitInfo()
        visitInfo2Direct = self.butler2.get("raw_visitInfo", self.dataId2a)  # noqa
        visitInfo3FromRaw = raw3.getInfo().getVisitInfo()
        visitInfo3Direct = self.butlerShim.get("raw_visitInfo", self.dataId3a)
        # Once again, Gen2 is not internally consistent, so we don't test
        # visitInfo2Direct.
        # Gen3 is internally consistent and consistent with getting the Gen2
        # VisitInfo from the full Exposure.
        # We compare strings to work around the fact that __eq__ is False when
        # some fields are NaN on both sides (it also makes for nicer failure
        # messages).
        self.assertEqual(str(visitInfo2FromRaw), str(visitInfo3FromRaw))
        self.assertEqual(str(visitInfo3FromRaw), str(visitInfo3Direct))

    def testDataRef(self):
        ref2 = self.butler2.dataRef("deepCoadd_det", dataId=self.dataId2b)
        ref3 = self.butlerShim.dataRef("deepCoadd_det", dataId=self.dataId3b)
        self.assertIs(ref2.butlerSubset.butler, self.butler2)
        self.assertIs(ref3.butlerSubset.butler, self.butlerShim)
        self.assertIs(ref2.getButler(), self.butler2)
        self.assertIs(ref3.getButler(), self.butlerShim)
        # Get a dataset of the type the DataRef was constructed with
        det2 = ref2.get()
        det3 = ref3.get()
        self.assertEqual(list(det2["id"]), list(det3["id"]))
        # Get a dataset of a different type (which also doesn't use one of
        # the data ID keys)
        mergeDet2 = ref2.get("deepCoadd_mergeDet")
        mergeDet3 = ref3.get("deepCoadd_mergeDet")
        self.assertEqual(list(mergeDet2["id"]), list(mergeDet3["id"]))

    def testPut(self):
        with TemporaryDirectory(dir=TESTDIR) as root:
            Butler3.makeRepo(root)
            butler3 = Butler3(root, run="three")
            butler3.registry.registerDatasetType(
                DatasetType("cat", ["label"], "SourceCatalog")
            )
            butlerShim = ShimButler(butler3)
            catIn = SourceCatalog(SourceCatalog.Table.makeMinimalSchema())
            catIn.addNew().set("id", 42)
            butlerShim.put(catIn, "cat", label="four")
            catOut = butlerShim.get("cat", label="four")
            self.assertEqual(list(catIn["id"]), list(catOut["id"]))
            # Without this the temporary directory can not be removed
            # if on NFS because these objects have open SQLite registries.
            del butler3
            del butlerShim


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
