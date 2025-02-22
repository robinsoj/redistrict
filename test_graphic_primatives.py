import unittest
from graphic_primatives import *

class TestPoint(unittest.TestCase):

    def test_init(self):
        point = Point(1, 2)
        self.assertEqual(point.x, 1)
        self.assertEqual(point.y, 2)

    def test_add(self):
        point1 = Point(1, 2)
        point2 = Point(3, 4)
        result = point1 + point2
        expected = Point(4, 6)
        self.assertEqual(result, expected)

    def test_str(self):
        point = Point(1, 2)
        self.assertEqual(str(point), "(1, 2)")

    def test_iter(self):
        point = Point(1, 2)
        x, y = point
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)

    def test_eq(self):
        point1 = Point(1, 2)
        point2 = Point(1, 2)
        point3 = Point(3, 4)
        self.assertTrue(point1 == point2)
        self.assertFalse(point1 == point3)

class TestLine(unittest.TestCase):

    def test_init_with_coordinates(self):
        line = Line(0, 0, 10, 10)
        self.assertEqual(line.p1, Point(0, 0))
        self.assertEqual(line.p2, Point(10, 10))
        self.assertEqual(line.color, "black")

    def test_init_with_points(self):
        p1 = Point(0, 0)
        p2 = Point(10, 10)
        line = Line(p1, p2)
        self.assertEqual(line.p1, p1)
        self.assertEqual(line.p2, p2)
        self.assertEqual(line.color, "black")

    def test_init_with_color(self):
        p1 = Point(0, 0)
        p2 = Point(10, 10)
        line = Line(p1, p2, color="red")
        self.assertEqual(line.color, "red")

    def test_draw(self):
        p1 = Point(0, 0)
        p2 = Point(10, 10)
        line = Line(p1, p2, color="blue")
        
        class MockCanvas:
            def create_line(self, x1, y1, x2, y2, fill, width):
                self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
                self.fill = fill
                self.width = width
        
        canvas = MockCanvas()
        line.draw(canvas)
        self.assertEqual(canvas.x1, 0)
        self.assertEqual(canvas.y1, 0)
        self.assertEqual(canvas.x2, 10)
        self.assertEqual(canvas.y2, 10)
        self.assertEqual(canvas.fill, "blue")
        self.assertEqual(canvas.width, 2)

class TestSquare(unittest.TestCase):

    def test_init(self):
        square = Square(1, 1, 4, 4, "blue")
        self.assertEqual(square.p1, Point(1, 1))
        self.assertEqual(square.p2, Point(4, 4))
        self.assertEqual(square.color, "blue")

    def test_draw_without_outline(self):
        square = Square(1, 1, 4, 4, "blue")
        
        class MockCanvas:
            def create_rectangle(self, x1, y1, x2, y2, fill, outline=None, width=None):
                self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
                self.fill = fill
                self.outline = outline
                self.width = width

        canvas = MockCanvas()
        square.draw(canvas)
        self.assertEqual(canvas.x1, 1)
        self.assertEqual(canvas.y1, 1)
        self.assertEqual(canvas.x2, 4)
        self.assertEqual(canvas.y2, 4)
        self.assertEqual(canvas.fill, "blue")
        self.assertIsNone(canvas.outline)
        self.assertIsNone(canvas.width)

    def test_draw_with_outline(self):
        square = Square(1, 1, 4, 4, "green")
        
        class MockCanvas:
            def create_rectangle(self, x1, y1, x2, y2, fill, outline=None, width=None):
                self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
                self.fill = fill
                self.outline = outline
                self.width = width

        canvas = MockCanvas()
        square.draw(canvas, outline=3)
        self.assertEqual(canvas.x1, 1)
        self.assertEqual(canvas.y1, 1)
        self.assertEqual(canvas.x2, 4)
        self.assertEqual(canvas.y2, 4)
        self.assertEqual(canvas.fill, "green")
        self.assertEqual(canvas.outline, 'yellow')
        self.assertEqual(canvas.width, 3)

class TestCircle(unittest.TestCase):

    def test_init(self):
        circle = Circle(3, 3, 5, "red")
        self.assertEqual(circle.p, Point(3, 3))
        self.assertEqual(circle.r, 5)
        self.assertEqual(circle.color, "red")

    def test_draw(self):
        circle = Circle(3, 3, 5, "red")
        
        class MockCanvas:
            def create_oval(self, x1, y1, x2, y2, fill):
                self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
                self.fill = fill
        
        canvas = MockCanvas()
        circle.draw(canvas)
        self.assertEqual(canvas.x1, -2)
        self.assertEqual(canvas.y1, -2)
        self.assertEqual(canvas.x2, 8)
        self.assertEqual(canvas.y2, 8)
        self.assertEqual(canvas.fill, "red")

class TestPolygon(unittest.TestCase):

    def test_init(self):
        points = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        polygon = Polygon("blue", points)
        self.assertEqual(polygon.points, points)
        self.assertEqual(polygon.color, "blue")
        self.assertEqual(polygon.fill_color, "grey")

    def test_draw(self):
        points = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        polygon = Polygon("blue", points)
        
        class MockCanvas:
            def create_polygon(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

        canvas = MockCanvas()
        polygon.draw(canvas)
        expected_flat_points = [0, 0, 1, 0, 1, 1, 0, 1]
        self.assertEqual(canvas.args[0], expected_flat_points)
        self.assertEqual(canvas.kwargs['outline'], "")
        self.assertEqual(canvas.kwargs['fill'], "grey")
        self.assertEqual(canvas.kwargs['width'], .5)

    def test_sides(self):
        points = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        polygon = Polygon("blue", points)
        expected_sides = [(points[0], points[1]), (points[1], points[2]), (points[2], points[3])]
        self.assertEqual(polygon.sides(), expected_sides)

    def test_gt(self):
        points1 = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        points2 = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        polygon1 = Polygon("blue", points1)
        polygon2 = Polygon("red", points2)

        # Mocking the area method
        Polygon.area = lambda self: 4 if self is polygon1 else 1
        
        self.assertTrue(polygon1 > polygon2)
        self.assertFalse(polygon2 > polygon1)

    def test_lt(self):
        points1 = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        points2 = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
        polygon1 = Polygon("blue", points1)
        polygon2 = Polygon("red", points2)

        # Mocking the area method
        Polygon.area = lambda self: 4 if self is polygon1 else 1
        
        self.assertTrue(polygon2 < polygon1)
        self.assertFalse(polygon1 < polygon2)

class TestSlider(unittest.TestCase):

    def test_init(self):
        labels = ["Low", "Medium", "High"]
        colors = ["red", "yellow", "green"]
        slider = Slider(0, 0, 0, 100, labels, colors)
        self.assertEqual(slider.p1, Point(0, 0))
        self.assertEqual(slider.p2, Point(0, 100))
        self.assertEqual(slider.labels, labels)
        self.assertEqual(slider.colors, colors)
        self.assertEqual(slider.level, 0)
        self.assertEqual(slider.y_delta, 40.0)
        self.assertEqual(slider.y_levels, [100.0, 60.0, 20.0])

    def test_draw(self):
        labels = ["Low", "Medium", "High"]
        colors = ["red", "yellow", "green"]
        slider = Slider(0, 0, 0, 100, labels, colors)
        
        class MockCanvas:
            def __init__(self):
                self.drawings = []

            def create_rectangle(self, x1, y1, x2, y2, fill, outline=None, width=None):
                self.drawings.append(('rectangle', x1, y1, x2, y2, fill, outline, width))

            def create_oval(self, x1, y1, x2, y2, fill):
                self.drawings.append(('oval', x1, y1, x2, y2, fill))

            def create_text(self, x, y, text, anchor, font):
                self.drawings.append(('text', x, y, text, anchor, font))

        canvas = MockCanvas()
        slider.draw(canvas)
        expected_drawings = [
            ('rectangle', 0, 0, 0, 100, 'red', None, None),
            ('rectangle', 10, 90, 15, 100.0, 'yellow', None, None),
            ('rectangle', 10, 100.0, 15, 10, 'green', None, None),
            ('oval', 2.5, 80.0, 22.5, 100.0, 'yellow'),
            ('text', 40, 90.0, 'Low', 'w', ('Helvetica', 11)),
            ('oval', 2.5, 40.0, 22.5, 60.0, 'green'),
            ('text', 40, 50.0, 'Medium', 'w', ('Helvetica', 11)),
            ('oval', 2.5, 0.0, 22.5, 20.0, 'green'),
            ('text', 40, 10.0, 'High', 'w', ('Helvetica', 11))
        ]
        self.assertEqual(canvas.drawings, expected_drawings)

    def test_on_click(self):
        labels = ["Low", "Medium", "High"]
        colors = ["red", "yellow", "green"]
        slider = Slider(0, 0, 0, 100, labels, colors)
        slider.on_click(type('Event', (object,), {'x': 0, 'y': 70})())
        self.assertEqual(slider.level, 1)
        slider.on_click(type('Event', (object,), {'x': 0, 'y': 30})())
        self.assertEqual(slider.level, 2)

    def test_get_level(self):
        labels = ["Low", "Medium", "High"]
        colors = ["red", "yellow", "green"]
        slider = Slider(0, 0, 0, 100, labels, colors)
        slider.level = 2
        self.assertEqual(slider.get_level(), 2)

if __name__ == '__main__':
    unittest.main()
