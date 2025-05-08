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
    test_county = 'maricopa'
    load_counties = [test_county]
    test_map = createTestMap()

    #stateData['districts'] = 1
    for county in stateData["counties"]:
        if county["county"] in load_counties:
            precintMap.update(createCountyPolygons(county))
    print("There are", len(precintMap), "precints in the JSON.")

    for k, v in precintMap.items():
        match = re.search(r'\d+$', k)
        if match:
            number = int(match.group())
            #if number >= 27 and number <= 33:
            if number in (210, 211, 233):
                for pt in v.boundaries.points:
                    print(f"{k},{pt.x},-{pt.y}")
                win.register_drawable(v.boundaries)
    #    win.register_drawable(v.boundaries)

    state = State(stateData["Name"], stateData["districts"], precintMap)
    #for precinct in state.precincts.values():
    #    if len(precinct.boundaries.points) < 3:
    #        precinct.assign_color(Color.DARK_MAGENTA.value, 10)
    #        print(precinct.name, len(precinct.boundaries.points))
    state.process_precincts()
    count = 0
    for precinct in state.precincts:
        if precinct[:len(test_county)] == test_county:
            state.precincts[precinct].assign_color(list(VGAColor)[count].value, count)
            count += 1
            if count > 9:
                count = 0
    #state.seed_initial_district()
    for k in test_map.keys():
        if k[:len(test_county)] == test_county:
           if (state.neighbor_map[k] != test_map[k]):
                print(f"{k}, {state.neighbor_map[k]}, {test_map[k]}")
    #print(state.neighbor_map['apache1'] == test_map['apache1'])
    #for i in range(len(test_map['apache1'])):
    #    print(state.neighbor_map['apache1'][i] == test_map['apache1'][i])
    #state.grab_neighboring_precinct(1)
    #state.grab_neighboring_precinct(1)
    #win.register_updateable(state)
    print("Trying to determine", stateData["districts"], "congressional districts")
    #print(state.precincts['apache1'].boundaries.points)
    #precinct1 = 'coconino7'
    #precinct2 = 'coconino53'
    #c1 = state.precincts[precinct1].boundaries.sides()
    #c2 = state.precincts[precinct2].boundaries.sides()
    #print(c1)
    #print(c2)
    #for i in range(1,75):
    #    prec = f'coconino{i}'
    #    print(i, state.precincts[prec].boundaries.sides())
    #print(state.are_polygons_connected(state.precincts[precinct1].boundaries, state.precincts[precinct2].boundaries))
    #print(state.is_point_on_line_segment(state.normalize_point(c1[3][0]), state.normalize_point(c2[3][0]), state.normalize_point(c2[3][1]), 4))
    #print(state.is_point_on_line_segment(c6[12][0], *c9[1]), state.is_point_on_line_segment(c6[12][1], *c9[1]),
    #      state.is_point_on_line_segment(c9[1][0], *c6[12]), state.is_point_on_line_segment(c9[1][1], *c6[12]))
    win.wait_for_close()


if __name__ == '__main__':
    main()
