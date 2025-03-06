import unittest
from district_census import *
from precinct import *

class TestDistrictCensus(unittest.TestCase):

    def setUp(self):
        self.census = District_Census()
        self.precinct1 = Precinct(boundaries=[], rep=10, dem=20, oth=5, name="Precinct1")
        self.precinct2 = Precinct(boundaries=[], rep=15, dem=10, oth=8, name="Precinct2")

    def test_initial_state(self):
        self.assertEqual(self.census.rep, 0)
        self.assertEqual(self.census.dem, 0)
        self.assertEqual(self.census.other, 0)

    def test_add_precinct(self):
        self.census.add_precinct(self.precinct1)
        self.assertEqual(self.census.rep, 10)
        self.assertEqual(self.census.dem, 20)
        self.assertEqual(self.census.other, 5)

        self.census.add_precinct(self.precinct2)
        self.assertEqual(self.census.rep, 25)
        self.assertEqual(self.census.dem, 30)
        self.assertEqual(self.census.other, 13)

    def test_remove_precinct(self):
        self.census.add_precinct(self.precinct1)
        self.census.add_precinct(self.precinct2)

        self.census.remove_precinct(self.precinct1)
        self.assertEqual(self.census.rep, 15)
        self.assertEqual(self.census.dem, 10)
        self.assertEqual(self.census.other, 8)

        self.census.remove_precinct(self.precinct2)
        self.assertEqual(self.census.rep, 0)
        self.assertEqual(self.census.dem, 0)
        self.assertEqual(self.census.other, 0)

if __name__ == '__main__':
    unittest.main()
