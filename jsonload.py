import json

with open("counties.json", 'r') as file:
    data = json.load(file)
    for county in data["counties"]:
        print(county["county"])
        for pt in county["boundary"]:
            print(" ", pt["x"], ", ", pt["y"])
