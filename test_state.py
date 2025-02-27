import unittest
from unittest.mock import patch, MagicMock
from graphic_primatives import *
from precinct import *
from state import *
from jsonload import *

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

    def setup_jsonload_state(self):
        stateData = openJson("test_county.json")
        precintList = []
        for county in stateData["counties"]:
            precintList.extend(createCountyPolygons(county))
        state = State(stateData["Name"], stateData["districts"], precintList)
        return state

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
    
    def test_is_polygon_inside(self):
        self.report_location()
        state = self.setup_jsonload_state()

        polygon1 = Polygon("black", state.precincts[0].boundaries)
        polygon2 = Polygon("black", state.precincts[1].boundaries)
        polygon3 = Polygon("black", state.precincts[2].boundaries)
        polygon4 = Polygon("black", state.precincts[3].boundaries)
        polygon5 = Polygon("black", state.precincts[4].boundaries)


        state.districts.append([])
        for precinct in state.precincts:
            state.update_district(precinct, 0)
            state.districts[0].append(precinct)

        self.assertTrue(state.is_polygon_inside(polygon2.points, state.districts[0]))
        self.assertTrue(state.is_polygon_inside(polygon3.points, state.districts[0]))
        self.assertTrue(state.is_polygon_inside(polygon1.points, state.districts[0]))
        self.assertFalse(state.is_polygon_inside(polygon1.points, []))
        nullPolygon = Polygon("black", [])
        self.assertFalse(state.is_polygon_inside(nullPolygon.points, state.districts[0]))

    def test_is_point_on_line_segment(self):
        self.report_location()
        point1 = Point(1, 1)
        point2 = Point(3, 3)
        point3 = Point(2, 2)
        point4 = Point(1, 2)
        point5 = Point(5, 5)

        st = self.set_up_state()

        self.assertTrue(st.is_point_on_line_segment(point3, point1, point2))
        self.assertFalse(st.is_point_on_line_segment(point4, point1, point2))
        self.assertFalse(st.is_point_on_line_segment(point1, point3, point2))
        self.assertFalse(st.is_point_on_line_segment(point5, point1, point2))

    @patch('random.choice')
    def test_seed_initial_district(self, mock_choice):
        self.report_location()
        state = self.setup_jsonload_state()
        mock_choice.side_effect = [state.precincts[1], state.precincts[2]]
        state.seed_initial_district()

        self.assertEqual(len(state.districts), 2)
        self.assertTrue(state.precincts[1] in state.districts[0])
        self.assertTrue(state.precincts[2] in state.districts[1])

        self.assertFalse(state.precincts[0] in state.districts[1])

if __name__ == '__main__':
    unittest.main()