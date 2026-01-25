def onCall():
    # this function is called whenever the ATC24 API is called
    #call the API from the HTTP server, then

    global x1, x2, y1, y2
    x1 = getInput.Float(1) #gets input from a composite, value 1
    x2 = getInput.Float(2) #value 2
    y1 = getInput.Float(3) #value 3
    y2 = getInput.Float(4) #value 4
def endFlight():
    #this function is called when the flight ends
    global dists
    dist_t = sum(dists)
    return dist_t


dists = []

while True:
    onCall()
    dists.append(((x2 - x1)**2 + (y2 - y1)**2)**0.5)

    if endFlight.triggered:
        endFlight()
        break
    