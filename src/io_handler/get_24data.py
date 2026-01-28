import asyncio
import json
from websockets.asyncio.client import connect as ws_connect

flight_queue = [] #flights for use in data-handler, stored [{data}, {data}, ...]
active_users = [] #list of all current users to be tracked

flight_queue_arr_dest = [] # only appends callsign(if ACA), arrival and departure airport

def filter_aca(flight_data_list):
    out = {}
    for callsign in flight_data_list:
        flight_info = flight_data_list[callsign] #dict of flight info WITHOUT callsign
        if (
            'Air Canadian' in callsign #must fly for air canada
            and flight_info['playerName'] in active_users #must participate in our logging sys
        ):
            out |= {callsign:flight_info} #append dict to output
    return out

async def load_data_to_queue(uri='wss://24data.ptfs.app/wss'): #open connection, then load new data
    async with ws_connect(uri) as websocket:
        while True:
            data_dump = await websocket.recv() #get json info
            data_dict = json.loads(data_dump) #load json info to dict
            
            if data_dict['t'] not in ['ACFT_DATA','EVENT_ACFT_DATA']: #only use acft data (standard OR event server)
                continue

            data_dict['d'] = filter_aca(data_dict['d']) #filter to only aca planes
            curr_time = data_dict['s'] #get current time for timestamp

            for callsign in data_dict['d']: #handle json data

                #NOTE: CALLSIGN IS INGAME CALLSIGN **NOT** PLAYER CHOSEN

                flight_dict={ #dict of flight info
                    **{'callsign':callsign},
                    **data_dict['d'][callsign],
                    **{'timestamp':curr_time},
                }
                flight_queue.append(flight_dict) #append to flight_queue
        
            flight_queue_arr_dest.append( #append to simplified arr/dep queue
                [
                    flight_dict['callsign': callsign],
                    flight_dict['arrivalAirport': arrivalAirport], #fix this pls thanks
                    flight_dict['departureAirport': departureAirport] # and this
                ]
            )

def start_loading_acft_data(): #start loading info to flight_queue
    asyncio.run(load_data_to_queue())
def get_flight_queue(): #easy fn to load current flight queue
    return flight_queue
