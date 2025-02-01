from tkinter import Tk, BOTH, Canvas
from graphic_primatives import *
from jsonload import *

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Congressional Redistricting"
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.bind("<Button-1>", self.on_click)
        self.__canvas.bind("<B1-Motion>", self.on_drag)
        self.__canvas.pack()
        self.__clickables = []
        self.__drawables = []
        self.running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True;
        while self.running:
            self.redraw()
            self.update_screen()

    def close(self):
        self.running = False
        self.__root.after(0, self.__root.quit)
        self.__root.destroy()

    def draw_line(self, line, color):
        line.draw(self.__canvas, color)

    def on_click(self, event):
        for clickable in self.__clickables:
            clickable.on_click(event)

    def on_drag(self, event):
        pass #determine where it is dropped

    def get_canvas(self):
        return self.__canvas

    def register_clickable(self, obj):
        self.__clickables.append(obj)

    def register_drawable(self, obj):
        self.__drawables.append(obj)

    def update_screen(self):
        if not self.running:
            return

        self.__canvas.delete("all")
        # TODO: draw the prescints

    def report_drawables(self):
        print(len(self.__drawables))

def main():
    win = Window(800, 600)
    stateData = openJson("counties.json")
    print(stateData["name"], "file was loaded")
    prescintList = createCountyPolygons(stateData["counties"][5])
    print("Trying to determine", stateData["districts"], "congressional districts")

    for poly in prescintList:
        win.register_drawable(poly)
        
    win.wait_for_close()


if __name__ == '__main__':
    main()
