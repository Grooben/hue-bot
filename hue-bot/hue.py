# A Hue Helper Python module that allows scripts
# to interact with Phillips Hue lighting systems.

import requests
import os
import json
from requests.exceptions import HTTPError
from dotenv import load_dotenv

load_dotenv()

bridge = os.getenv('BRIDGE_IP')
token = os.getenv('H_TOKEN')
restURL = "http://{0}/api/{1}".format(bridge, token)

def getRequestHandler(endpoint):
    """Handles get requests.
     Kwargs:
     endpoint -- the endpoint url the request should be sent to, for example; lights/1/on
    """
    url = "{0}/{1}".format(restURL, endpoint)
    try:
        response = requests.get(url)
    except HTTPError as e:
        print("A HTTP Error has occurred: {0}".format(e))
    except Exception as e:
        print("wtf: {0}".format(e))
    else:
        response = response.json()
    return response

def putRequestHandler(endpoint, req):
    """Handles put requests.
     Kwargs:
     endpoint -- the endpoint url the request should be sent to, for example; lights/1/on
     req -- the body of the request to be sent to the endpoint
    """
    url = "{0}/{1}".format(restURL, endpoint)
    req = json.dumps(req)
    try:
        response = requests.put(url, data=req)
    except HTTPError as e:
        print("A HTTP Error has occurred: {0}".format(e))
    except Exception as e:
        print("wtf: {0}".format(e))
    else:
        return
    return

def getLights():
    lights = getRequestHandler("lights")
    return lights

def getLightStatusSimp(id):
    lights = getLights()
    state = "On" if lights[str(id)]["state"]["on"] else "Off"
    # some hue lights aren't rgb, and thus they don't send a hue value
    # so we need to deal with that
    try:
        colHue = lights[str(id)]["state"]["hue"]
    except Exception as e:
        colHue = "RGB Lighting is not supported by this light."
    statusStr = "ID: {0}\nState: {1}\nColour (Hue): {2}".format(id, state, colHue)
    return statusStr

def getLightStatusDetailed(id):
    lights = getLights()
    state = "On" if lights[str(id)]["state"]["on"] else "Off"
    type = lights[str(id)]["type"]
    swVer = lights[str(id)]["swversion"]
    updStatus = "No" if lights[str(id)]["swupdate"]["state"] == "noupdates" else "Yes"
    try:
        colHue = lights[str(id)]["state"]["hue"]
    except Exception as e:
        colHue = "RGB Lighting is not supported by this light."
    statusStr = "State: {0}\nColour (hue): {1}\nType: {2}\nSoftware version: {3}\nUpdate Needed?: {4}".format(state, colHue, type, swVer, updStatus)
    return statusStr
    
# endpoint url for each individual light is "lights/(lightId)/endpoint"
def turnOnLight(id):
    """Turns on an individual light.
    Kwargs:
    id -- the id of the light to turn on
    """
    endpoint = "lights/{0}/state".format(id)
    req = {"on":True}
    putRequestHandler(endpoint, req)
    return 

def turnOffLight(id):
    """Turns off an individual light.
    Kwargs:
    id -- the id of the light to turn off
    """
    endpoint = "lights/{0}/state".format(id)
    req = {"on":False}
    putRequestHandler(endpoint, req)
    return 