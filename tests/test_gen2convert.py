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

import lsst.utils.tests
import lsst.afw.image.testUtils  # noqa; injects test methods into TestCase
from lsst.utils import getPackageDir
from lsst.daf.butler import Butler


REPO_ROOT = os.path.join(getPackageDir("ci_hsc"), "DATA")
TESTDIR = os.path.abspath(os.path.dirname(__file__))


class Gen2ConvertTestCase(lsst.utils.tests.TestCase):

    def setUp(self):
        self.butler = Butler(REPO_ROOT, run="shared/ci_hsc")

    def tearDown(self):
        del self.butler

    def testImpliedDimensions(self):
        """Test that implied dimensions are expanded properly when populating
        the Dataset table.
        """
        # All of the dataset types below have Visit or Exposure in their
        # dimensions, which means PhysicalFilter and AbstractFilter are
        # implied. dimensions for them.  Those should be non-null and
        # consistent.
        sql = """
            SELECT physical_filter, abstract_filter
            FROM Dataset
            WHERE dataset_type_name IN (
                'raw', 'calexp', 'icExp', 'src', 'icSrc',
                'deepCoadd_directWarp', 'deepCoadd_psfMatchedWarp'
            )
            """
        count = 0
        for row in self.butler.registry.query(sql):
            if row["physical_filter"] == "HSC-R":
                self.assertEqual(row["abstract_filter"], "r")
            elif row["physical_filter"] == "HSC-I":
                self.assertEqual(row["abstract_filter"], "i")
            else:
                self.fail("physical_filter not in ('HSC-R', 'HSC-I')")
            count += 1
        self.assertGreater(count, 0)


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
