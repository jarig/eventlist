import math
from _ext.foursquare.models import Foursquare
from _ext.foursquare import settings as fqSettings

__author__ = 'jarik'


def getFourSquareVenues(region, step=2):
    """
    Get all foursquare venues from given region
    region - 4 item tuple [swN,swE,neN,neE]
    step - optional parameter specifying quadrature step in KM
    """
    EARTH_RAD = 6371 #km
    foursquareAPI = Foursquare(
        client_id=fqSettings.CLIENT_ID,
        client_secret=fqSettings.CLIENT_SECRET
    )
    #convert grads to degrees
    for i in range(len(region)):
        region[i] = gradToDec(region[i])

    #split region into sub-regions and go through each getting
    hGradChange = abs(region[3] - region[1])
    vGradChange = abs(region[2] - region[0])
    horizontalDistance = (hGradChange*math.pi*EARTH_RAD)/180
    verticalDistance = (vGradChange*math.pi*EARTH_RAD)/180
    hSteps = int(horizontalDistance/step+1)
    vSteps = int(verticalDistance/step+1)
    print "Horizontal Distance: %s" % horizontalDistance
    print "Vertical Distance: %s" % verticalDistance
    print "Total steps: %s" % int(hSteps*vSteps)

    gradStep = (step * 180)/(math.pi*EARTH_RAD)
    result = None
    for hStep in range(hSteps):
        hDegree = region[1] + gradStep * hStep #move right
        for vStep in range(vSteps):
            vDegree = region[0] + gradStep * vStep #move up
            sub_region =  [vDegree, hDegree, vDegree+gradStep, hDegree+gradStep]
            venues = foursquareAPI.venues.search(params={ 'sw': '%0.6f,%0.6f ' % (decToGrad(sub_region[0]), decToGrad(sub_region[1])),
                                                          'ne': '%0.6f,%0.6f ' % (decToGrad(sub_region[2]), decToGrad(sub_region[3])),
                                                          'intent':'browse', 'limit':50, 'venuePhotos': 1 })
            print "Region: sw=%s,%s&ne=%s,%s ; results: %d" % (decToGrad(sub_region[0]),
                                                               decToGrad(sub_region[1]),
                                                               decToGrad(sub_region[2]),
                                                               decToGrad(sub_region[3]),len(venues["venues"]))
            if result is None:
                result = venues
            else:
                result["venues"].extend(venues["venues"])
    return result

def gradToDec(grad):
    integer = int(grad)
    decimal = (grad - integer)/0.6
    return integer + decimal

def decToGrad(decim):
    degree = int(decim)
    minutes =  (decim - float(degree))*0.6
    return degree + minutes