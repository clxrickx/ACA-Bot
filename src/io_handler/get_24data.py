import asyncio
from json import loads
from websockets.asyncio.client import connect

users_to_track = [] #current list of all users to be tracked

flight_profiles = [] #flight profiles for use in data handler, stored [{data}, {data}, ...], eligible acft only
acft_data_queue = [] #flights for use in data-handler, stored [{data}, {data}, ...], eligible acft only

def is_fp_eligible(flight_profile):
    return (
        'Air Canadian' in flight_profile['realcallsign'] #must fly for air canada
        and flight_profile['robloxName'] in users_to_track #must participate in our logging sys
    )
def filter_acft_data(flight_data_list):
    out = {}
    for callsign in flight_data_list:
        flight_info = flight_data_list[callsign] #dict of flight info WITHOUT callsign
        if (
            'Air Canadian' in callsign #must fly for air canada
            and flight_info['playerName'] in users_to_track #must participate in our logging sys
        ):
            out |= {callsign:flight_info} #append dict to output
    return out # returns all aca flights as dicts where the callsign is the key

async def load_data_to_queue(uri='wss://24data.ptfs.app/wss'): #open connection, then load new data
    async with connect(uri) as websocket:
        while True:
            data_dump = await websocket.recv() #get json info
            data_dict = loads(data_dump) #load json info to dict

            #NOTE 'callsign' field in data_dict is ingame callsign NOT user-chosen callsign
            
            if data_dict['t'] in ['ACFT_DATA','EVENT_ACFT_DATA']: #acft data (standard OR event server)

                data_dict['d'] = filter_acft_data(data_dict['d']) #filter to only eligible aca flights
                curr_time = data_dict['s'] #get current time for timestamp

                for callsign in data_dict['d']: #handle json data
                    flight_dict={ #dict of flight info
                        **{'callsign':callsign},
                        **data_dict['d'][callsign],
                        **{'timestamp':curr_time},
                    }
                    acft_data_queue.append(flight_dict) #append to acft_data_queue
            
            elif data_dict['t'] in ['FLIGHT_profile', 'EVENT_FLIGHT_profile']: #filed flight profile (standard OR event server)

                flight_profile = data_dict['d'] #get flight profile

                if (
                    is_fp_eligible(flight_profile) #signed up AND flying aca
                    and flight_profile not in flight_profiles #avoid duplicates
                ):
                    for other_fp in flight_profiles:
                        if other_fp['robloxName'] == flight_profile['robloxName']:
                            flight_profiles.remove(other_fp)
                            break

                    flight_profiles.append(flight_profile) #add to fp list
            
            else: #if new info is NOT acft data or flight profile
                continue #for readability's sake

def start_loading_acft_data(): #start loading info to acft_data_queue
    asyncio.run(load_data_to_queue())

def get_acft_data_queue(): #easy fn to load current flight queue
    return acft_data_queue
def get_flight_profiles(): #easy fn to load current flight profiles
    return flight_profiles