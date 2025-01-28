class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

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
    def __init__(self, x, y, color, points):
        self.center = Point(x, y)
        self.lines = []
        if points is not None:
            prev_point = points[0]
            for i in range(len(points)):
                if points[i] != prev_point:
                    line = Line(prev_point, points[i], color=color)
                    self.lines.append(line)
                    prev_point = points[i]
            line = Line(prev_point, points[0], color=color)
            self.lines.append(line)
        self.color = color

    def draw(self, canvas):
        if canvas is None:
            return
        for line in self.lines:
            line.draw(canvas)
        self.first = False
                

class Switch:
    def __init__(self, x1, y1, x2, y2, label, color1, color2):
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)
        self.label = label
        self.color1 = color1
        self.color2 = color2
        self.status = False
        self.click = self.on_click

    def on_click(self, event):
        x1 = min(self.p1.x, self.p2.x)
        x2 = max(self.p1.x, self.p2.x)
        y1 = min(self.p1.y, self.p2.y)
        y2 = max(self.p1.y, self.p2.y)
        if x1 <= event.x and event.x <= x2 and y1 <= event.y and event.y <= y2:
            self.status = not self.status

    def draw(self, canvas):
        if canvas is None:
            return
        midx = (self.p1.x + self.p2.x) / 2
        canvas.create_text(midx, self.p1.y - 15, text=self.label,
                           font=("Helvetica", 20))
        canvas.create_rectangle(self.p1.x, self.p1.y,
                                self.p2.x, self.p2.y,
                                fill=self.color1)
        if self.status:
            canvas.create_rectangle(midx, self.p1.y + 10,
                                    self.p2.x - 10, self.p2.y - 10,
                                    fill=self.color2)
        else:
            canvas.create_rectangle(self.p1.x + 10, self.p1.y + 10,
                                    midx, self.p2.y - 10,
                                    fill=self.color2)

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
        label_font = ("Helcetica", 11)

        sq0 = Square(self.p1.x, self.p1.y, self.p2.x, self.p2.y, self.colors[0])
        sq1 = Square(x_min + 5, y_max, x_min, y_mid, self.colors[1])
        sq2 = Square(x_min + 5, y_mid, x_min, y_min, self.colors[2])

        sq0.draw(canvas)
        sq1.draw(canvas)
        sq2.draw(canvas)

        for y in range(len(self.labels)):
            if (y <= self.level):
                color = self.colors[1]
            else:
                color = self.colors[2]
            cir_x = x_min + 2.5
            cir_y = y_max - y * self.y_delta
            circle = Circle(cir_x, cir_y, 10, color)
            circle.draw(canvas)
            label_text = f"{self.labels[y]}"
            canvas.create_text(x_min + 30, cir_y,
                               text=label_text, anchor="w",
                               font=label_font)

    def on_click(self, event):
        x1 = min(self.p1.x, self.p2.x)
        x2 = max(self.p1.x, self.p2.x)
        y1 = min(self.p1.y, self.p2.y)
        y2 = max(self.p1.y, self.p2.y)
        if x1 <= event.x and event.x <= x2 and y1 <= event.y and event.y <= y2:
            for pl in range(len(self.y_levels)):
                if (event.y < self.y_levels[pl]):
                    self.level = pl

    def get_level(self):
        return self.level
        
class Turn_Indicator:
    def __init__(self, x, y, length, width):
        self.active = True
        self.label_text = "Turn: "
        self.x = x
        self.y = y + width/2
        self.square = Square(x + 35, y, x + length - 25, y + width, '#000000')

    def draw(self, canvas):
        canvas.create_text(self.x, self.y, text=self.label_text, anchor="w",
                           font=("Helvetica", 11))
        self.square.draw(canvas)

    def flip_turn(self):
        self.active = not self.active
        if not self.active:
            self.square.color = "#FF0000"
        else:
            self.square.color = "#000000"

    def on_click(self, event):
        x = event.x
        y = event.y
        if x < self.x or y < self.y or x > self.square.p2.x or y > self.square.p2.y:
            return None
        self.flip_turn()
