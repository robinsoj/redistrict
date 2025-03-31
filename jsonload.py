import json
import queue
from graphic_primatives import *
from precinct import *

def openJson(stateFile):
    with open(stateFile, 'r') as file:
        data = json.load(file)
        #for county in data["counties"]:
        #    print(county["county"])
        #    for pt in county["boundary"]:
        #        print(" ", pt["x"], ", ", pt["y"])
        #print(data["districts"])
    return data

def createCountyPolygons(countyJson):
    print("Processing:", countyJson["county"])
    ret_list = []
    precinctCount = len(countyJson["precincts"])
    rep = round(countyJson["rep"]/precinctCount)
    dem = round(countyJson["dem"]/precinctCount)
    oth = round(countyJson["oth"]/precinctCount)
    for precinct in countyJson["precincts"]:
        points = []
        for i in precinct["boundary"]:
            point = Point(i["x"]+10, i["y"]+10)
            points.append(point)
        pg = Polygon("grey", points)
        precinctItem = Precinct(pg, rep, dem, oth, countyJson["county"] + str(precinct["id"]))
        ret_list.append(precinctItem)
    return ret_list
