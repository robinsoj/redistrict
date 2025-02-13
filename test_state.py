import unittest
from graphic_primatives import *
from precinct import *
from state import *

class Tests(unittest.TestCase):
    def test_are_polygons_connected(self):
        points1 = [Point(0, 0), Point(100, 0), Point(100, 100), Point(0,0)]
        points2 = [Point(0, 0), Point(100, 0), Point(100, -100), Point(0,0)]
        points3 = [Point(0, 0), Point(100, -100), Point(50, -100), Point(0, 0)]
        pg1 = Polygon("black", points1)
        pg2 = Polygon("black", points2)
        pg3 = Polygon("black", points3)

        precinct = Precinct([pg1, pg2, pg3], 0, 0, 0, "Test County")
        st = State("Test", 1, precinct)

        test1 = st.are_polygons_connected(pg1, pg2) #Should be true
        test2 = st.are_polygons_connected(pg1, pg3) #Should be false
        test3 = st.are_polygons_connected(pg2, pg3) #Should be true

        print(test1, test2, test3)
        
        self.assertEqual(test1, True)
        self.assertEqual(test2, False)
        self.assertEqual(test3, True)

if __name__ == '__main__':
    unittest.main()