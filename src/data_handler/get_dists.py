from asyncio import sleep
from io_handler.get_24data import start_loading_acft_data
from io_handler.get_24data import get_acft_data_queue, get_flight_profiles

cartesian_dist = lambda x1,y1,x2,y2: ((x2-x1)**2 + (y2-y1)**2)**0.5
# studs_to_NM = lambda studs: studs/3307.14286 #uses 3307.14286 studs/NM, 0.56m/stud, as stated in 24data server

def select_fp_by_username(flight_profiles, username):
    for flight_profile in flight_profiles:
        if flight_profile['robloxName'] == username:
            return flight_profile
    raise KeyError('data_handler.get_dists.select_fp_by_username: no flight profile with username found')

def calculate_next_dist():
    #TEMP NOTE: this fn will need to be called in main.py for each iteration, preferably between fp + acft data updates
    #TEMP NOTE: likely will need to rework the async stuff to be able to schedule this b/w 24data update calls

    flight_profiles = get_flight_profiles() #stores as reference
    acft_data_queue = get_acft_data_queue() #also stores as reference

    for new_acft_data in acft_data_queue:
        roblox_username = new_acft_data['playerName']
        flight_profile = select_fp_by_username(flight_profiles, roblox_username)
        
        if 'studsTraveled' not in flight_profile: #first hit
            flight_profile['studsTraveled'] = 0 #initialize studs traveled value
            flight_profile['lastPositionStuds'] = ( #initialize last position value
                new_acft_data['position']['x'], #x,y positions are in studs
                new_acft_data['position']['y']
            )
        else: #any hit after first
            current_position = ( #get current position
                new_acft_data['position']['x'],
                new_acft_data['position']['y']
            )
            flight_profile['studsTraveled'] += cartesian_dist( #add new dist
                *current_position, #current position
                *flight_profile['lastPositionStuds'], #last position
            )
            flight_profile['lastPositionStuds'] = current_position #update last position
        
        acft_data_queue.remove(new_acft_data)#clear current acft data instance from queue

# distsSpeed = []

# dep_arr_basic = [] #list of [callsign, arrival, departure]

# #this loop will be in effect while accurate distance calculations are being made
# while True:
#     # backup printout from the live callsign-keyed dict (added system)
#     for callsign, info in dep_arr_basic_live.items():
#         arrivalAero = info.get("arrivalAirport")
#         departureAero = info.get("departureAirport")
#         print(f"{callsign}: {departureAero} -> {arrivalAero}")
#     break

# exit()

# #remove accurate calculations for now at least until i/o handling is completed
# while True:
#     sleep(3)
#     for i in range(len(flight_data)-1):
#         acft1 = flight_data[i]
#         acft2 = flight_data[i+1]

#         # Calculate Cartesian distance
#         dx = acft2['x'] - acft1['x']
#         dy = acft2['y'] - acft1['y']
#         dz = acft2['z'] - acft1['z']
#         dist_cartesian = (dx**2 + dy**2 + dz**2)**0.5
#         distsCartesian.append(dist_cartesian)

#         # Calculate Speed difference
#         speed_diff = abs(acft2['speed'] - acft1['speed'])
#         distsSpeed.append(speed_diff)