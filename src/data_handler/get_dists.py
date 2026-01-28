import time
from src.io_handler.get_24data import flight_queue

def slp(seconds):
    time.sleep(seconds)

flights_tracked = []
flight_data = flight_queue.copy() #get current flight data

distsCartesian = []
distsSpeed = []

#this loop will be in effect while accurate distance calculations are being made
while True:

    break

exit()

#remove accurate calculations for now at least until i/o handling is completed
while True:
    slp(3)
    for i in range(len(flight_data)-1):
        acft1 = flight_data[i]
        acft2 = flight_data[i+1]

        # Calculate Cartesian distance
        dx = acft2['x'] - acft1['x']
        dy = acft2['y'] - acft1['y']
        dz = acft2['z'] - acft1['z']
        dist_cartesian = (dx**2 + dy**2 + dz**2)**0.5
        distsCartesian.append(dist_cartesian)

        # Calculate Speed difference
        speed_diff = abs(acft2['speed'] - acft1['speed'])
        distsSpeed.append(speed_diff)
    
