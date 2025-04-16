class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter((self.x, self.y))
    
    def __eq__(self, point):
        tolerance = .1
        return abs(self.x - point.x) < tolerance and abs(self.y - point.y) < tolerance
    
    def __lt__(self, point):
        return self.x < point.x and self.y < point.y

    def __gt__(self, point):
        return self.x > point.x and self.y > point.y
    
    def __sub__(self, point):
        return Point(abs(self.x - point.x), abs(self.y - point.y))

class Line:
    def __init__(self, *args, color="black"):
        if len(args) == 4:
            self.p1 = Point(args[0], args[1])
            self.p2 = Point(args[2], args[3])
        elif len(args) == 2 and all(isinstance(arg, Point) for arg in args):
            self.p1 = args[0]
            self.p2 = args[1]
        self.color = color

    def draw(self, canvas):
        if canvas is None:
            return
        canvas.create_line(self.p1.x, self.p1.y,
                           self.p2.x, self.p2.y,
                           fill=self.color,
                           width=2)

class Square:
    def __init__(self, x1, y1, x2, y2, color):
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)
        self.color = color

    def draw(self, canvas, outline = None):
        if canvas is None:
            return
        if outline is None:
            canvas.create_rectangle(self.p1.x, self.p1.y,
                                    self.p2.x, self.p2.y,
                                    fill=self.color)
        else:
            canvas.create_rectangle(self.p1.x, self.p1.y,
                                    self.p2.x, self.p2.y,
                                    outline='yellow',
                                    fill=self.color,
                                    width=outline)

class Circle:
    def __init__(self, x, y, r, color):
        self.p = Point(x, y)
        self.r = r
        self.color = color

    def draw(self, canvas):
        if canvas is None:
            return
        canvas.create_oval(self.p.x - self.r, self.p.y - self.r,
                           self.p.x + self.r, self.p.y + self.r,
                           fill=self.color)

class Polygon:
    def __init__(self, color, points):
        if points is not None:
            self.points = points
        self.color = color
        self.fill_color = color

    def __gt__(self, other):
        return self.area() > other.area()
    
    def __lt__(self, other):
        return self.area() < other.area()

    def draw(self, canvas):
        if canvas is None:
            return
        flat_points = [int(coord) for point in self.points for coord in (point.x, point.y)]
        canvas.create_polygon(flat_points, outline=self.color, fill=self.fill_color, width=1)

    def sides(self):
        ret_val = []
        for i in range(len(self.points)-1):
            ret_val.append((self.points[i], self.points[i+1]))
        ret_val.append((self.points[-1], self.points[0]))
        #return [(self.points[i], self.points[i + 1]) for i in range(len(self.points) - 1)]
        return ret_val
    
class Slider:
    def __init__(self, x1, y1, x2, y2, labels, colors):
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)
        self.labels = labels
        self.colors = colors
        self.level = 0
        self.y_levels = []
        y_dist = abs(y1 - y2) - 20
        y_min = max(y1, y2)
        self.y_delta = y_dist / (len(labels) - 1)
        for y in range(len(labels)):
            self.y_levels.append(y_min - y * self.y_delta)

    def draw(self, canvas):
        y_mid = self.y_levels[self.level]
        x_min = min(self.p1.x, self.p2.x) + 10
        y_min = min(self.p1.y, self.p2.y) + 10
        y_max = max(self.p1.y, self.p2.y) - 10
        label_font = ("Helvetica", 11)

        sq0 = Square(self.p1.x, self.p1.y, self.p2.x, self.p2.y, self.colors[0])
        sq1 = Square(x_min + 5, y_max, x_min, y_mid, self.colors[1])
        sq2 = Square(x_min + 5, y_mid, x_min, y_min, self.colors[2])

        sq0.draw(canvas)
        sq1.draw(canvas)
        sq2.draw(canvas)

        for y in range(len(self.labels)):
            if y <= self.level:
                color = self.colors[1]
            else:
                color = self.colors[2]
            cir_x = x_min + 2.5
            cir_y = y_max - y * self.y_delta
            circle = Circle(cir_x, cir_y, 10, color)
            circle.draw(canvas)
            label_text = f"{self.labels[y]}"
            canvas.create_text(x_min + 30, cir_y, text=label_text, anchor="w", font=label_font)

    def on_click(self, event):
        x1 = min(self.p1.x, self.p2.x)
        x2 = max(self.p1.x, self.p2.x)
        y1 = min(self.p1.y, self.p2.y)
        y2 = max(self.p1.y, self.p2.y)
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            for pl in range(len(self.y_levels)):
                if (event.y < self.y_levels[pl]):
                    self.level = pl

    def get_level(self):
        return self.level
