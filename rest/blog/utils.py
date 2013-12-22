import logging
import math
from _ext.foursquare.models import Foursquare
from _ext.foursquare import settings as fqSettings

logger = logging.getLogger(__name__)

REGIONS = {
    "Estonia":
    {
        "Tallinn": [59.336691, 24.528008, 59.536407, 25.084877]
    }
}


def importFoursqaureVenus(country, city=None):
    cities = REGIONS[country]
    if city is None:
        cities = REGIONS[country]
    imported = 0
    for key in cities:
        logger.info("Importing: %s" % key)
        result = getFourSquareVenues(REGIONS[country][key])
        imported += len(result)
    pass


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
    horizontalDistance = (hGradChange * math.pi * EARTH_RAD) / 180
    verticalDistance = (vGradChange * math.pi * EARTH_RAD) / 180
    hSteps = int(horizontalDistance / step + 1)
    vSteps = int(verticalDistance / step + 1)
    totalSteps = int(hSteps * vSteps)
    print "Horizontal Distance: %s" % horizontalDistance
    print "Vertical Distance: %s" % verticalDistance
    print "Total steps: %s" % totalSteps

    gradStep = (step * 180) / (math.pi * EARTH_RAD)
    result = None
    counter = 0
    for hStep in range(hSteps):
        hDegree = region[1] + gradStep * hStep #move right
        for vStep in range(vSteps):
            vDegree = region[0] + gradStep * vStep #move up
            sub_region = [vDegree, hDegree, vDegree + gradStep, hDegree + gradStep]
            venues = foursquareAPI.venues.search(
                params={'sw': '%0.6f,%0.6f ' % (decToGrad(sub_region[0]), decToGrad(sub_region[1])),
                        'ne': '%0.6f,%0.6f ' % (decToGrad(sub_region[2]), decToGrad(sub_region[3])),
                        'intent': 'browse', 'limit': 50, 'venuePhotos': 1})
            counter += 1
            perc = (counter / totalSteps) * 100
            print "Region: sw=%s,%s&ne=%s,%s ; results: %d %d%%" % (decToGrad(sub_region[0]),
                                                                    decToGrad(sub_region[1]),
                                                                    decToGrad(sub_region[2]),
                                                                    decToGrad(sub_region[3]), len(venues["venues"]),
                                                                    perc)
            if result is None:
                result = venues
            else:
                result["venues"].extend(venues["venues"])
    return result


def gradToDec(grad):
    integer = int(grad)
    decimal = (grad - integer) / 0.6
    return integer + decimal


def decToGrad(decim):
    degree = int(decim)
    minutes = (decim - float(degree)) * 0.6
    return degree + minutes