from tkinter import Tk, BOTH, Canvas
from graphic_primatives import *
from jsonload import *
from precinct import *
from state import *
from test_map import *
import re

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Congressional Redistricting"
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        #self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas = Canvas(self.__root, width=width, height=height, background="black")
        self.__canvas.bind("<Button-1>", self.on_click)
        self.__canvas.bind("<B1-Motion>", self.on_drag)
        self.__canvas.pack()
        self.__clickables = []
        self.__drawables = []
        self.__updateables = []
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
    
    def register_updateable(self, obj):
        self.__updateables.append(obj)

    def update_screen(self):
        if not self.running:
            return
        
        for updateable in self.__updateables:
            updateable.update()

        self.__canvas.delete("all")
        for drawable in self.__drawables:
            drawable.draw(self.__canvas)

    def report_drawables(self):
        print(len(self.__drawables))

def main():
    win = Window(820, 620)
    stateData = openJson("counties.json")
    print(stateData["Name"], "file was loaded")
    precintMap = {}
    load_counties = ['apache', 'cochise', 'coconino', 'gila', 'graham', 'greenlee', 'la_paz', 'maricopa', 'mohave',
                     'navajo', 'pima', 'pinal', 'santa_cruz', 'yavapai', 'yuma']

    #stateData['districts'] = 1
    for county in stateData["counties"]:
        if county["county"] in load_counties:
            precintMap.update(createCountyPolygons(county))
    print("There are", len(precintMap), "precints in the JSON.")

    state = State(stateData["Name"], stateData["districts"], precintMap)

    state.process_precincts()

    state.seed_initial_district()
    print("Trying to determine", stateData["districts"], "congressional districts")
    win.wait_for_close()


if __name__ == '__main__':
    main()
