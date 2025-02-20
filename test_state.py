import unittest
from graphic_primatives import *
from precinct import *
from state import *
import inspect

class Tests(unittest.TestCase):
    def report_location(self):
        caller_frame = inspect.stack()[1]
        caller_name = caller_frame.function
        print(f"Executing: {caller_name}")
    
    def set_up_state(self):
        points1 = [Point(0, 0), Point(100, 0), Point(100, 100), Point(0,0)]
        points2 = [Point(0, 0), Point(100, 0), Point(100, -100), Point(0,0)]
        points3 = [Point(0, 0), Point(100, -100), Point(50, -100), Point(0, 0)]
        points4 = [Point(0,0,), Point(50,50), Point(0, 100), Point(0,0)]
        points5 = [Point(0,100), Point(50, 50), Point(100, 100), Point(0, 100)]
        points6 = [Point(0,0), Point(0, 50), Point(-50, 0), Point(0, 0)]
        points7 = [Point(0, 0), Point(0, -100), Point(-100, 0), Point(0,0)]
        points8 = [Point(-50, 0), Point(-100, 0), Point(0, 100), Point(0, 50), Point(-50, 0)]
        points9 = [Point(0,0), Point(50, -100), Point(0, -100), Point(0, 0)]

        pg1 = Polygon("black", points1)
        pg2 = Polygon("black", points2)
        pg3 = Polygon("black", points3)
        pg4 = Polygon("black", points4)
        pg5 = Polygon("black", points5)
        pg6 = Polygon("black", points6)
        pg7 = Polygon("black", points7)
        pg8 = Polygon("black", points8)
        pg9 = Polygon("black", points9)

        precincts = [
            Precinct([pg1], 0, 0, 0, "Test County"),
            Precinct([pg2], 0, 0, 0, "Test County"),
            Precinct([pg3], 0, 0, 0, "Test County"),
            Precinct([pg4], 0, 0, 0, "Test County"),
            Precinct([pg5], 0, 0, 0, "Test County"),
            Precinct([pg6], 0, 0, 0, "Test County"),
            Precinct([pg7], 0, 0, 0, "Test County"),
            Precinct([pg8], 0, 0, 0, "Test County"),
            Precinct([pg9], 0, 0, 0, "Test County")
        ]
    
        st = State("Test", 1, precincts)
        return st
    
    def test_are_polygons_connected(self):
        self.report_location()
        st = self.set_up_state()

        pg1 = st.precincts[0].boundaries[0]
        pg2 = st.precincts[1].boundaries[0]
        pg3 = st.precincts[2].boundaries[0]
        pg4 = st.precincts[3].boundaries[0]

        test1 = st.are_polygons_connected(pg1, pg2) #Should be true
        test2 = st.are_polygons_connected(pg1, pg3) #Should be false
        test3 = st.are_polygons_connected(pg2, pg3) #Should be true
        test4 = st.are_polygons_connected(pg4, pg1) #Should be true

        self.assertEqual(test1, True)
        self.assertEqual(test2, False)
        self.assertEqual(test3, True)
        self.assertEqual(test4, True)

    def test_is_point_inside_polygon(self):
        self.report_location()
        st = self.set_up_state()
        pg1 = st.precincts[0].boundaries[0].points

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
    
    def setUp(self):
        # Set up some example polygons and precincts
        self.polygon1 = Polygon("black", [Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)]) # A square
        self.polygon2 = Polygon("black", [Point(1, 1), Point(3, 1), Point(3, 3), Point(1, 3)]) # Smaller square inside polygon1
        self.polygon3 = Polygon("black", [Point(5, 5), Point(7, 5), Point(7, 7), Point(5, 7)]) # Another square outside polygon1

        self.precinct1 = Precinct([self.polygon1],0, 0, 0, "Test")
        self.precinct2 = Precinct([self.polygon2],0, 0, 0, "Test")
        self.precinct3 = Precinct([self.polygon3],0, 0, 0, "Test")

        self.st = State("Test", 1, [self.precinct1, self.precinct2, self.precinct3])

    def test_polygon_inside(self):
        self.assertTrue(self.st.is_polygon_inside(self.polygon2, [self.precinct1]))
        self.assertFalse(self.st.is_polygon_inside(self.polygon3, [self.precinct1]))

    def test_polygon_outside(self):
        self.assertFalse(self.st.is_polygon_inside(self.polygon1, [self.precinct2]))
        self.assertTrue(self.st.is_polygon_inside(self.polygon1, [self.precinct1, self.precinct2]))

    def test_empty_precincts(self):
        self.assertFalse(self.st.is_polygon_inside(self.polygon1, []))

    def test_empty_polygon(self):
        self.assertFalse(self.st.is_polygon_inside(Polygon("black", []), [self.precinct1]))

if __name__ == '__main__':
    unittest.main()