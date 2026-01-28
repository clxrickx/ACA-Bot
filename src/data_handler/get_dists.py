import json

def load_flight_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

flight_data = data = load_flight_data('src/io_handler/get_24data.py')

distsCartesian = []
distsSpeed = []

while True:
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
