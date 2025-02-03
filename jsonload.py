import json
import queue
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
        point = Point(i["x"], i["y"])
        points.append(point)
    points.append(points[0])
    pg = Polygon("black", points)
    prescincts = countyJson["prescints"] - 1
    power = 0
    while (1 << power) < prescincts:
        pg = pg.subdivide()
        power += 1
    pq = queue.PriorityQueue()
    pq.put((pg.area()*-1, pg))
    while prescincts > 0:
        item = pq.get()
        item2 = item[1].subdivide()
        p1, p2 = item2.divide()
        if p1 is not None:
            pq.put((p1.area()*-1, p1))
        if p2 is not None:
            pq.put((p2.area()*-1, p2))
        prescincts -= 1
    ret_list = []
    while not pq.empty():
        ret_list.append(pq.get()[1])
    return ret_list
