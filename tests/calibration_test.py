# Copyright (C) 2018  Charlie Hoy <charlie.hoy@ligo.org>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from pesummary.gw.file.calibration import CalibrationDict, Calibration
import numpy as np
import os
import shutil


class TestCalibrationDict(object):
    """Test that the CalibrationDict works as expected
    """
    def setup(self):
        """Setup the testing class
        """
        self.calibration_data = {
            "H1": [[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                   [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]],
            "L1": [[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                   [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]],
        }
        
    def test_initiate(self):
        """Test that the PSDDict class can be initalized correctly
        """
        cal_dict = CalibrationDict(
            self.calibration_data.keys(), self.calibration_data.values()
        )
        assert sorted(list(cal_dict.detectors)) == ["H1", "L1"]
        assert isinstance(cal_dict["H1"], Calibration)
        np.testing.assert_almost_equal(
            cal_dict["H1"].frequencies, [0, 0.0]
        )
        np.testing.assert_almost_equal(
            cal_dict["L1"].phase_upper, [0.6, 0.6]
        )

        cal_dict = CalibrationDict(self.calibration_data)
        assert sorted(list(cal_dict.detectors)) == ["H1", "L1"]
        assert isinstance(cal_dict["H1"], Calibration)
        np.testing.assert_almost_equal(
            cal_dict["H1"].frequencies, [0, 0.0]
        )
        np.testing.assert_almost_equal(
            cal_dict["L1"].phase_upper, [0.6, 0.6]
        )


class TestCalibration(object):
    """Test the Calibration class
    """
    def setup(self):
        """Setup the testing class
        """
        self.obj = Calibration([[1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7]])
        if not os.path.isdir(".outdir"):
            os.mkdir(".outdir")

    def teardown(self):
        """Remove all files and directories created from this class
        """
        if os.path.isdir(".outdir"):
            shutil.rmtree(".outdir")

    def test_save_to_file(self):
        """Test the save to file method
        """
        self.obj.save_to_file(".outdir/test.dat")
        data = np.genfromtxt(".outdir/test.dat")
        np.testing.assert_almost_equal(data.T[0], [1, 1])
        np.testing.assert_almost_equal(data.T[1], [2, 2])

    def test_invalid_input(self):
        """Test that the appropiate error is raised if the input is wrong
        """
        import pytest

        with pytest.raises(IndexError):
            obj = Calibration([10, 10])
