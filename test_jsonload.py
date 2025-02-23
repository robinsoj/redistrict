import unittest
import json
import queue
from graphic_primatives import Point, Polygon
from precinct import Precinct
from jsonload import *

# Sample JSON data for testing
json_data = '''{
    "Name": "Test",
    "counties": [
        {
            "county": "Test",
            "precincts": [
                {
                    "id": 1,
                    "boundary": [
                        {"x": 0.0, "y": 0.0},
                        {"x": 1.0, "y": 0.0},
                        {"x": 1.0, "y": 1.0},
                        {"x": 0.0, "y": 1.0},
                        {"x": 0.0, "y": 0.0}
                    ]
                },
                {
                    "id": 2,
                    "boundary": [
                        {"x": 0.0, "y": 0.0},
                        {"x": 0.0, "y": 1.0},
                        {"x": -1.0, "y": 1.0},
                        {"x": -1.0, "y": 0.0},
                        {"x": 0.0, "y": 0.0}
                    ]
                },
                {
                    "id": 3,
                    "boundary": [
                        {"x": 0.0, "y": 0.0},
                        {"x": 0.0, "y": -1.0},
                        {"x": -1.0, "y": -1.0},
                        {"x": -1.0, "y": 0.0},
                        {"x": 0.0, "y": 0.0}
                    ]
                },
                {
                    "id": 4,
                    "boundary": [
                        {"x": 0.0, "y": 0.0},
                        {"x": 1.0, "y": 0.0},
                        {"x": 1.0, "y": -1.0},
                        {"x": 0.0, "y": -1.0},
                        {"x": 0.0, "y": 0.0}
                    ]
                }
            ],
            "rep": 5824,
            "dem": 18016,
            "oth": 8160
        }
    ],
    "districts": 8
}'''

class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.test_data = json.loads(json_data)

    def test_openJson(self):
        # Test openJson function assuming 'test_state.json' exists
        data = openJson('test_county.json')
        self.assertEqual(data, self.test_data)

    def test_createCountyPolygons(self):
        county_json = self.test_data['counties'][0]
        precincts = createCountyPolygons(county_json)
        
        self.assertEqual(len(precincts), 4)
        self.assertEqual(precincts[0].name, 'Test')
        self.assertEqual(precincts[0].rep, 1456)
        self.assertEqual(precincts[0].dem, 4504)
        self.assertEqual(precincts[0].oth, 2040)
        self.assertIsInstance(precincts[0].boundaries, Polygon)
        self.assertEqual(precincts[0].boundaries.points[0].x, 10)
        self.assertEqual(precincts[0].boundaries.points[0].y, 10)
        self.assertEqual(precincts[0].boundaries.fill_color, 'grey')

if __name__ == '__main__':
    unittest.main()
