"""Make sure PYTHONPATH environment variable is set to access cdippy package"""

import unittest
from datetime import datetime, timedelta
import os

import numpy as np

# CDIP imports
import cdippy.cdipnc as nc
import cdippy.stndata as sd
import cdippy.mopdata as md
import cdippy.ncstats as ns
import cdippy.nchashes as nh
import cdippy.url_utils as uu
import cdippy.location as loc
import cdippy.ndbc as ndbc
import cdippy.spectra as sp


def get_active_datasets(dataset_name):
    url = (
        "http://thredds.cdip.ucsd.edu/thredds/catalog/cdip/"
        + dataset_name
        + "/catalog.xml"
    )
    root = uu.load_et_root(url)
    datasets = []
    uu.rfindta(root, datasets, "dataset", "name")
    return datasets


def convert_date(date_str):
    """From '2022-05-26T01:02:03Z' to '2022-05-26 01:02:03'"""
    return date_str[0:10] + " " + date_str[11:19]


class TestCdipnc(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_url(self):
        a = nc.Archive("100p1", data_dir="https://cdip.ucsd.edu")
        self.assertEqual(
            a.url, "https://cdip.ucsd.edu/thredds/dodsC/cdip/archive/100p1/100p1_d01.nc"
        )

    def test_data_path(self):
        a = nc.Archive("100p1", data_dir="/project/WNC/WNC_DATA")
        self.assertEqual(a.url, "/project/WNC/WNC_DATA/ARCHIVE/100p1/100p1_d01.nc")

    def test_active_predeploy(self):
        dataset_names = get_active_datasets("predeploy")
        r = None
        if len(dataset_names) > 0:
            for dn in dataset_names:
                if "_rt" in dn:
                    stn = dn[0:3]
                    dep = int(dn[7:9])
                    a = nc.Active(stn, dep, "predeploy")
                    r = {}
                    if a is not None:
                        a.set_request_info(pub_set="all")
                        r = a.get_request()
                    self.assertTrue("waveTime" in r and len(r["waveTime"]) > 0)
                    break
        else:
            self.assertTrue(1 == 1)  # Pass the test if no predeploy datasets


class TestMopData(unittest.TestCase):

    def setUp(self):
        # Dates within an existing archive deployment BP100
        now = datetime.utcnow()
        now_day = now.strftime("%Y-%m-%d")
        self.dt1 = now_day + " 00:00:00"
        self.dt2 = now_day + " 23:59:59"
        self.v = ["waveHs"]

    def tearDown(self):
        self.dt1 = None
        self.dt2 = None
        self.v = None

    def test_read_nc_data(self):
        m = md.MopData("BP100", "nowcast")
        d = m.get_series(self.dt1, self.dt2, self.v)
        self.assertEqual(len(d["waveHs"]), 13)

    def test_target_records(self):
        m = md.MopData("BP100", "nowcast")
        d = m.get_series(self.dt1, None, self.v, target_records=6)
        self.assertEqual(len(d["waveHs"]), 7)

    def test_parameters(self):
        m = md.MopData("BP100", "nowcast")
        d = m.get_parameters(self.dt1, self.dt2)
        self.assertEqual(len(d.keys()), 5)
        self.assertTrue("waveDp" in d.keys())

    def test_spectra(self):
        m = md.MopData("BP100", "nowcast")
        d = m.get_spectra(self.dt1, self.dt2)
        self.assertEqual(len(d.keys()), 8)
        self.assertTrue("waveA1Value" in d.keys())

    def test_url(self):
        m = md.MopData("BP100", "ecmwf_fc")
        self.assertEqual(
            m.url,
            "https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/model/MOP_validation/BP100_ecmwf_fc.nc",
        )

    def test_meta(self):
        m = md.MopData("BP100", "ecmwf_fc")
        d = m.get_mop_meta()
        self.assertTrue("time_coverage_start" in d.keys())
        self.assertEqual(len(d.keys()), 16)

    def test_ecmwf_fc(self):
        m = md.MopData("BP100", "ecmwf_fc")
        meta = m.get_mop_meta()
        start = convert_date(meta["time_coverage_start"])
        d = m.get_series(start, vrs=self.v, target_records=60)
        self.assertEqual(len(d.keys()), 2)
        self.assertEqual(len(d["waveHs"]), 61)

    def test_alongshore(self):
        m = md.MopData("D0001", "forecast")
        meta = m.get_mop_meta()
        start = convert_date(meta["time_coverage_start"])
        d = m.get_series(start, vrs=self.v, target_records=60)
        self.assertEqual(len(d.keys()), 2)
        self.assertEqual(len(d["waveHs"]), 61)


class TestSpectra(unittest.TestCase):

    def setUp(self):
        # Station and dates within an existing archive deployment
        self.s100 = sd.StnData("100p1")
        self.dt_100_1 = "2017-10-16 00:00:00"
        self.dt_100_2 = "2017-10-16 01:00:00"

        # Station and dates that cross deployments of mk3 and mk4
        self.s142 = sd.StnData("142p1")
        self.dt_142_1 = "2017-01-24 00:00:00"
        self.dt_142_2 = "2017-02-25 12:00:00"

        # Station and dates that cross deployments of mk4 mk3
        self.s260 = sd.StnData("260p1")
        self.dt_260_1 = "2024-04-24 00:00:00"
        self.dt_260_2 = "2024-04-26 00:00:00"

        # Station and dates that cross historic and realtime (mk4 to mk3)
        # There should be 202 waveTime and spectrum should have 64 bands.
        self.s271 = sd.StnData("271p1")
        self.dt_271_1 = "2023-09-20 00:00:00"
        self.dt_271_2 = "2023-10-14 00:00:00"
        # We should check that the values for the 2d vars in historic match
        # after we redistribute.
        self.dt_271_3 = "2023-09-20 00:00:00"
        self.dt_271_4 = "2023-09-24 00:00:00"

        self.dt_271_5 = "2023-10-12 00:00:00"
        self.dt_271_6 = "2023-10-14 00:00:00"

    def tearDown(self):
        self.s = None
        self.dt1 = None
        self.dt2 = None
        self.v = None

    def test_redistribute(self):
        data = self.s100.get_spectra(self.dt_100_1, self.dt_100_2)
        self.assertEqual(len(data["waveEnergyDensity"]), 2)
        s = sp.Spectra()
        s.set_spectrumArr_fromQuery(data)
        self.assertEqual(s.get_spectraNum(), 2)
        self.assertEqual(s.get_bandSize(), 64)
        s.redist_specArr("Spectrum_9band")
        self.assertEqual(s.get_bandSize(), 9)
        s.redist_specArr("Spectrum_100band")
        self.assertEqual(s.get_bandSize(), 100)
        data = s.specArr_ToDict()
        self.assertTrue("waveA1Value" in data.keys())
        self.assertTrue(len(data["waveA1Value"][0]) == 100)
        self.assertTrue("waveCheckFactor" in data.keys())
        self.assertTrue(len(data["waveCheckFactor"][0]) == 100)

    def test_mk3mk4_redistribute(self):
        # !IMPORTANT!
        # This is a temporary test that will not work once the current
        # realtime depoyment of Oct 2023 is completed. At that point
        # the historic file will be converted to the mk 3 spectral layout.
        # !IMPORTANT!

        # The historic.nc file contains only the mk4 spectral layout
        # and the realtime.nc file contains the mk3 spectral layout.

        # Show that the historic data is 100 band
        data_mk4 = self.s271.get_spectra(self.dt_271_3, self.dt_271_4)
        self.assertEqual(data_mk4["waveEnergyDensity"].shape, (175, 100))

        # Test the concatenation and redistribution to 64 bands
        data = self.s271.get_spectra(self.dt_271_1, self.dt_271_2)
        self.assertEqual(data["waveEnergyDensity"].shape, (202, 64))

        # Test the force_64bands option on the historic data
        data_mk4 = self.s271.get_spectra(
            self.dt_271_3, self.dt_271_4, force_64bands=True
        )
        self.assertEqual(data_mk4["waveEnergyDensity"].shape, (175, 64))


class TestStnData(unittest.TestCase):

    def setUp(self):
        self.s = sd.StnData("100p1")
        # Dates within an existing archive deployment
        self.dt1 = "2017-10-16 00:00:00"
        self.dt2 = "2017-10-16 01:00:00"
        self.v = ["waveHs"]

    def tearDown(self):
        self.s = None
        self.dt1 = None
        self.dt2 = None
        self.v = None

    def test_read_nc_data(self):
        d = self.s.get_series(self.dt1, self.dt2, self.v)
        self.assertEqual(len(d["waveHs"]), 2)

    def test_pub_set_and_mask(self):
        # Tests mask
        d = self.s.get_series(self.dt1, self.dt2, self.v, "nonpub")
        self.assertEqual(len(d["waveHs"]), 0)
        d = self.s.get_series(self.dt1, self.dt2, self.v, "nonpub", False)
        self.assertEqual(len(d["waveHs"]), 2)
        # Tests pub_set (TODO: Need to use a timespan with both public and nonpub data
        d = self.s.get_series(self.dt1, self.dt2, self.v, "public")
        self.assertEqual(len(d["waveHs"]), 2)
        d = self.s.get_series(self.dt1, self.dt2, self.v, "all")
        self.assertEqual(len(d["waveHs"]), 2)

    def test_across_deployments(self):
        d = self.s.get_series(
            "2007-05-30 00:00:00", "2007-06-01 23:59:59", ["xyzData"], "public"
        )
        self.assertEqual(len(d["xyzTime"]), 304127)

    def test_target_records(self):
        d = self.s.get_series(self.dt1, None, self.v, target_records=6)
        self.assertEqual(len(d["waveHs"]), 7)

    def test_get_nc_files(self):
        # d = self.s.get_nc_files()
        # self.assertTrue('100p1_d01.nc' in d.keys())
        pass

    def test_ww3(self):
        s = sd.StnData("100p1", org="ww3")
        d = s.get_series("2016-08-01 23:00:00", "2016-08-01 23:59:59", ["waveHs"])
        self.assertEqual(len(d["waveHs"]), 1)

    def test_stn_meta(self):
        d = self.s.get_stn_meta()
        self.assertTrue("geospatial_lon_min" in d.keys())

    def test_mark1_filter_delay(self):
        s = sd.StnData("071p1")
        end = datetime(1996, 1, 22, 15, 57, 00)
        start = end - timedelta(hours=2)
        d = s.get_xyz(start, end)
        self.assertEqual(len(d["xyzTime"]), 9216)

    def test_use_archive_if_no_moored_hs(self):
        s = sd.StnData("100p1", deploy_num=15)
        d = s.get_series(self.dt1, self.dt2, ["waveHs"])
        self.assertEqual(len(d["waveHs"]), 2)

    def test_use_archive_if_no_moored_xyz(self):
        s = sd.StnData("100p1", deploy_num=15)
        d = s.get_series(self.dt1, self.dt2, ["xyzZDisplacement"])
        self.assertEqual(len(d["xyzZDisplacement"]), 4608)

    def test_stn_meta_deploy_num(self):
        dataset_names = get_active_datasets("predeploy")
        if len(dataset_names) > 0:
            for dn in dataset_names:
                if "_rt" in dn:
                    stn = dn[0:3]
                    dep = int(dn[7:9])
                    s = sd.StnData(stn, deploy_num=dep)
                    r = s.get_stn_meta()
                    self.assertTrue("metaStationName" in r)
                    break
        else:
            self.assertTrue(1 == 1)  # Ok if no predeploy datasets

    def test_get_gps_for_old_deployment(self):
        s = sd.StnData("142p3", deploy_num=14)
        d = s.get_series("1975-12-20 00:00:00", "2019-01-31 23:59:59", s.gps_vars)
        self.assertTrue("gpsLatitude" in d and len(d["gpsLatitude"]) > 0)

    def test_remove_duplicates(self):
        dd = {}
        dd["waveTime"] = np.array([1, 2, 3, 2, 4])
        dd["waveHs"] = np.array([0.1, 0.2, 0.3, 0.2, 0.4])
        r = self.s.remove_duplicates(dd)
        self.assertTrue(len(r["waveTime"]) == 4 and r["waveHs"][3] == 0.4)


class TestLatest(unittest.TestCase):

    def setUp(self):
        self.latest = nc.Latest()

    def tearDown(self):
        self.latest = None

    def test_get_latest(self):
        d = self.latest.get_latest(
            pub_set="both-all",
            meta_vars=[
                "metaLongitude",
                "metaLatitude",
                "metaWaterDepth",
                "metaDeployLabel",
                "metaWMOid",
            ],
            params=[
                "waveHs",
                "sstSeaSurfaceTemperature",
                "gpsLatitude",
                "gpsLongitude",
                "acmSpeed",
                "acmDirection",
            ],
        )
        self.assertEqual("gpsLatitude" in d, True) and self.assertEqual(
            "groupTime" in d, True
        ) and self.assertEqual("sstTimeBounds" in d, True) and self.assertEqual(
            "metaWMOid" in d, True
        )


class TestNcStats(unittest.TestCase):

    def setUp(self):
        self.stats = ns.NcStats("100p1")

    def tearDown(self):
        self.stats = None

    def test_summary(self):
        summary = self.stats.deployment_summary()
        self.assertEqual(
            summary["d12"]["time_coverage_start"], datetime(2013, 12, 13, 22, 0, 0)
        )


class TestNcHashes(unittest.TestCase):

    def setUp(self):
        self.hashes = nh.NcHashes()

    def tearDown(self):
        self.hashes = None
        os.remove("HASH.pkl")
        # os.remove('WMO_IDS.pkl')

    def test_compare_hash_tables(self):
        self.hashes.save_new_hashes()
        self.hashes.load_hash_table()
        compare = self.hashes.compare_hash_tables()
        self.assertEqual(len(compare), 0)


class TestLocation(unittest.TestCase):

    def setUp(self):
        lat1 = 21.6689
        lon1 = -158.1156
        lat2 = 21.66915
        lon2 = -158.11487
        self.l1 = loc.Location(lat1, lon1)
        self.l2 = loc.Location(lat2, lon2)

    def tearDown(self):
        self.l1 = None
        self.l2 = None

    def test_write_loc(self):
        self.assertEqual(self.l1.write_loc(), "21.6689 N -158.1156")

    def test_decimal_min_loc(self):
        self.assertEqual(self.l1.decimal_min_loc()["mlat"], "40.134")

    def test_get_distance(self):
        self.assertEqual(self.l1.get_distance(self.l2), 0.04342213936740085)

    def test_get_distance_formatted(self):
        self.assertEqual(self.l1.get_distance_formatted(self.l2), "0.04")


class TestNDBC(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        os.remove("./WMO_IDS.pkl")

    def test_get_wmo_id(self):
        self.assertEqual(ndbc.get_wmo_id("100"), "46225")


# How to run a single method
# suite = unittest.TestLoader().loadTestsFromName('test_cdippy.TestSpectra.test_mk3mk4_redistribute')
# suite = unittest.TestLoader().loadTestsFromName('test_cdippy.TestSpectra.test_redistribute')
# unittest.TextTestRunner(verbosity=2).run(suite)
# sys.exit(0)

# How to run all tests in a specified class
# suite = unittest.TestLoader().loadTestsFromTestCase(TestSpectra)
# unittest.TextTestRunner(verbosity=2).run(suite)
# sys.exit(0)

# Adding tests to a test suite
suite = unittest.TestSuite()
cdipnc_suite = unittest.TestLoader().loadTestsFromTestCase(TestCdipnc)
mopdata_suite = unittest.TestLoader().loadTestsFromTestCase(TestMopData)
stndata_suite = unittest.TestLoader().loadTestsFromTestCase(TestStnData)
latest_suite = unittest.TestLoader().loadTestsFromTestCase(TestLatest)
ncstat_suite = unittest.TestLoader().loadTestsFromTestCase(TestNcStats)
nchash_suite = unittest.TestLoader().loadTestsFromTestCase(TestNcHashes)
ndbc_suite = unittest.TestLoader().loadTestsFromTestCase(TestNDBC)
spectra_suite = unittest.TestLoader().loadTestsFromTestCase(TestSpectra)
suite.addTests(
    [
        cdipnc_suite,
        mopdata_suite,
        stndata_suite,
        latest_suite,
        ncstat_suite,
        nchash_suite,
        ndbc_suite,
        spectra_suite,
    ]
)
# suite.addTests([ncstat_suite])

unittest.TextTestRunner(verbosity=2).run(suite)
