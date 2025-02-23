import unittest
from graphic_primatives import Polygon
from precinct import Precinct

class TestPrecinct(unittest.TestCase):

    def setUp(self):
        self.boundary = Polygon(color=None, points=[(0, 0), (1, 0), (1, 1), (0, 1)])
        self.precinct1 = Precinct(boundaries=self.boundary, rep=100, dem=150, oth=50, name='Precinct 1')
        self.precinct2 = Precinct(boundaries=None, rep=200, dem=100, oth=75, name='Precinct 2')

    def test_initialization(self):
        self.assertEqual(self.precinct1.name, 'Precinct 1')
        self.assertEqual(self.precinct1.rep, 100)
        self.assertEqual(self.precinct1.dem, 150)
        self.assertEqual(self.precinct1.oth, 50)
        self.assertEqual(self.precinct1.district, -1)
        self.assertIsInstance(self.precinct1.boundaries, Polygon)
        self.assertEqual(self.precinct1.boundaries.fill_color, "grey")
        
        self.assertEqual(self.precinct2.name, 'Precinct 2')
        self.assertIsNone(self.precinct2.boundaries)

    def test_assign_color(self):
        color = 'red'
        district = 1
        self.precinct1.assign_color(color, district)
        self.assertEqual(self.precinct1.boundaries.fill_color, color)
        self.assertEqual(self.precinct1.district, district)

if __name__ == '__main__':
    unittest.main()
