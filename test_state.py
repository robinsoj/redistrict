import unittest
from graphic_primatives import *
from precinct import *
from state import *

class Tests(unittest.TestCase):
    def set_up_state(self):
        points1 = [Point(0, 0), Point(100, 0), Point(100, 100), Point(0,0)]
        points2 = [Point(0, 0), Point(100, 0), Point(100, -100), Point(0,0)]
        points3 = [Point(0, 0), Point(100, -100), Point(50, -100), Point(0, 0)]
        pg1 = Polygon("black", points1)
        pg2 = Polygon("black", points2)
        pg3 = Polygon("black", points3)

        precinct = Precinct([pg1, pg2, pg3], 0, 0, 0, "Test County")
        st = State("Test", 1, precinct)
        return st
    
    def test_are_polygons_connected(self):
        st = self.set_up_state()

        pg1 = st.precincts.boundaries[0]
        pg2 = st.precincts.boundaries[1]
        pg3 = st.precincts.boundaries[2]

        test1 = st.are_polygons_connected(pg1, pg2) #Should be true
        test2 = st.are_polygons_connected(pg1, pg3) #Should be false
        test3 = st.are_polygons_connected(pg2, pg3) #Should be true
        
        self.assertEqual(test1, True)
        self.assertEqual(test2, False)
        self.assertEqual(test3, True)

    def test_is_point_inside_polygon(self):
        st = self.set_up_state()

        pg1 = st.precincts.boundaries[0].points

        p1 = Point(50, 25)
        p2 = Point(0,0)
        p3 = Point(100, -100)
        p4 = Point(75, 25)

        test1 = st.is_point_inside_polygon(p1, pg1) #Should be true
        test2 = st.is_point_inside_polygon(p2, pg1) #Should be true
        test3 = st.is_point_inside_polygon(p3, pg1) #Should be false
        test4 = st.is_point_inside_polygon(p4, pg1) #Should be true

        self.assertEqual(test1, True)
        self.assertEqual(test2, True)
        self.assertEqual(test3, False)
        self.assertEqual(test4, True)

if __name__ == '__main__':
    unittest.main()