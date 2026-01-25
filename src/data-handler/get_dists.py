def getInputCartesian():
    global x1, x2, y1, y2
    x1 = getInput.Float(1) #gets input from a composite, value 1
    x2 = getInput.Float(2) #value 2
    y1 = getInput.Float(3) #value 3
    y2 = getInput.Float(4) #value 4

def getInputSpeed():
    global s, h, alt1, alt2
    s = getInput.Float(5) #gets input from a composite, value 5, speed
    h = getInput.Float(6) #value 6 (heading)
    alt1 = getInput.Float(7) #value 7 (altitude)
    #alt2 is previous altitude from last API call
    alt2 = 0#placeholder value; actual implementation depends on API response

def onCall():
    # this function is called whenever the ATC24 API is called
    #call the API from the HTTP server, then
    getInputCartesian()
    getInputSpeed()
    global t
    #time interval between calls, in seconds, find the time interval from the API call
    t = 1 # Placeholder value; actual implementation depends on API response


def endFlight():
    #this function is called when the flight ends
    global distsCartesian, distsSpeed
    if sum(distsSpeed) - 10 < sum(distsCartesian) or sum(distsSpeed) + 10 > sum(distsCartesian):
        print("Warning: Distance by speed does not match distance by coordinates!")
        #put Joe's data here for output
    dist_t = sum(distsCartesian)
    return dist_t


distsCartesian = []
distsSpeed = []

while True:
    onCall()
    distNowCartesian = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    # Correct horizontal displacement from speed by removing the vertical component
    # Vertical change (dz) between the two altitude readings
    dz = abs(alt2 - alt1)
    # slant distance travelled (magnitude of displacement) from speed*time
    slant = s * t
    # horizontal component = sqrt(slant^2 - dz^2) when slant >= dz
    if slant >= dz:
        distNowSpeed = (slant**2 - dz**2)**0.5
    else:
        # If altitude change exceeds slant distance due to measurement error,
        # set horizontal displacement to 0 and warn
        distNowSpeed = 0.0
        print("Warning: altitude change ({:.3f}) larger than distance travelled ({:.3f}); setting horizontal displacement to 0".format(dz, slant))
    distsCartesian.append(distNowCartesian)
    distsSpeed.append(distNowSpeed)
    # update previous altitude for next iteration
    alt2 = alt1
    if endFlight.triggered:
        endFlight()
        break