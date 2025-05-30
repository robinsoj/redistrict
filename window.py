from tkinter import Tk, BOTH, Canvas, Text, Scrollbar, NW, VERTICAL, Frame, LEFT, RIGHT
from graphic_primatives import *
from jsonload import *
from precinct import *
from state import *
from test_map import *
import re
import sys

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Congressional Redistricting")
        self.__root.geometry(f"{width}x{height}")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__main_frame = Frame(self.__root)
        self.__main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.__canvas = Canvas(self.__main_frame, width=600, height=600)
        #self.__canvas = Canvas(self.__main_frame, width=width, height=height, background="black")
        self.__canvas.bind("<Button-1>", self.on_click)
        self.__canvas.bind("<B1-Motion>", self.on_drag)
        self.__canvas.pack(side=LEFT, padx=5, pady=5)

        self.__text_frame = Frame(self.__main_frame)
        self.__text_frame.pack(side=RIGHT, fill=BOTH, expand=False, anchor="n")

        self.__text = Text(self.__text_frame, height=10, width=150, bg="white")
        self.__text.pack(side=LEFT, fill="none", expand=False, anchor="n")
        
        self.__scrollbar = Scrollbar(self.__text_frame, orient=VERTICAL, command=self.__text.yview)
        self.__scrollbar.pack(side='right', fill='x')
        self.__text.config(yscrollcommand=self.__scrollbar.set)
        
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
            if type(updateable) == State:
                self.update_district_numbers(updateable.generate_district_counts())
            updateable.update()

        self.__canvas.delete("all")
        for drawable in self.__drawables:
            drawable.draw(self.__canvas)

    def report_drawables(self):
        print(len(self.__drawables))

    def update_district_numbers(self, str):
        self.__text.delete("1.0", "end")
        self.__text.insert("end", str)

def main(arg1):
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
    for k, v in precintMap.items():
        win.register_drawable(v.boundaries)
    if arg1 == "":
        state.process_precincts()
    else:
        state.process_precincts(createTestMap())

    #actual logic begin
    state.seed_initial_district()
    print("Trying to determine", stateData["districts"], "congressional districts")
    win.register_updateable(state)
    win.wait_for_close()
    #actual logic end

    #populate all precincts to one district except for one.
    #call find_adjacent_precincts until I find an error.
    #dist_list = []
    #for precinct in state.precincts:
    #    state.update_district(precinct, 0)
    #    dist_list.append(precinct)
    #state.districts.append(dist_list)
    #dist_list2 = []
    #state.update_district('maricopa51', 1)
    #dist_list2.append('maricopa51')
    #state.districts.append(dist_list2)
    #choices = ['maricopa65', 'maricopa79', 'maricopa78', 'maricopa77', 'maricopa63']
    #for item in choices:
    #    state.districts[state.precincts[item].district].remove(item)
    #    state.districts[1].append(item)
    #    state.update_district(item, 1)
    #print('maricopa50' in state.find_adjacent_precincts(1))

if __name__ == '__main__':
    param1 = ""
    try:
        if sys.argv is not None:
            param1 = sys.argv[1]
    except:
        print("Fresh mode")
    main(param1)
