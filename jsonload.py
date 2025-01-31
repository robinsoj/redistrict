import json
from graphic_primatives import *

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
    points = []
    for i in countyJson["boundary"]:
        point = Point(i["x", "y"])
        points.append(point)
    points.append(points[0])
    pg = Polygon("black", points)
    prescincts = countyJson["prescincts"]
    power = 0
    while (1 << power) < prescincts:
        pg = pg.subdivide()
    #TODO Add logic to divde the Polygon into the number of prescincts
