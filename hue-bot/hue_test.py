import hue
import json
from pprint import pprint

lights = hue.getLights()

count = 1
while(count <= len(lights)):
    pprint(lights[str(count)]["name"])
    pprint(lights[str(count)]["state"])
    count = count + 1