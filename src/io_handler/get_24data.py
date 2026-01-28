import asyncio
import json
from websockets.asyncio.client import connect as ws_connect

active_users = [] #list of all current users to be tracked

flight_plans = [] #flight plans for use in data handler, stored [{data}, {data}, ...], eligible acft only
acft_data_queue = [] #flights for use in data-handler, stored [{data}, {data}, ...], eligible acft only

def is_fp_eligible(flight_plan):
    return (
        'Air Canadian' in flight_plan['realcallsign'] #must fly for air canada
        and flight_plan['robloxName'] in active_users #must participate in our logging sys
    )
def filter_acft_data(flight_data_list):
    out = {}
    for callsign in flight_data_list:
        flight_info = flight_data_list[callsign] #dict of flight info WITHOUT callsign
        if (
            'Air Canadian' in callsign #must fly for air canada
            and flight_info['playerName'] in active_users #must participate in our logging sys
        ):
            out |= {callsign:flight_info} #append dict to output
    return out # returns all aca flights as dicts where the callsign is the key

async def load_data_to_queue(uri='wss://24data.ptfs.app/wss'): #open connection, then load new data
    async with ws_connect(uri) as websocket:
        while True:
            data_dump = await websocket.recv() #get json info
            data_dict = json.loads(data_dump) #load json info to dict

            #NOTE 'callsign' field in data_dict is ingame callsign NOT user-chosen callsign
            
            if data_dict['t'] in ['ACFT_DATA','EVENT_ACFT_DATA']: #acft data (standard OR event server)

                data_dict['d'] = filter_acft_data(data_dict['d']) #filter to only eligible aca planes
                curr_time = data_dict['s'] #get current time for timestamp

                for callsign in data_dict['d']: #handle json data
                    flight_dict={ #dict of flight info
                        **{'callsign':callsign},
                        **data_dict['d'][callsign],
                        **{'timestamp':curr_time},
                    }
                    acft_data_queue.append(flight_dict) #append to acft_data_queue
            
            elif data_dict['t'] in ['FLIGHT_PLAN', 'EVENT_FLIGHT_PLAN']: #filed flight plan (standard OR event server)

                flight_plan = data_dict['d'] #get flight plan

                if (
                    is_fp_eligible(flight_plan) #signed up AND flying aca
                    and flight_plan not in flight_plans #avoid duplicates
                ):
                    flight_plans.append(flight_plan)
            
            else: #otherwise
                continue #for readability's sake

def start_loading_acft_data(): #start loading info to acft_data_queue
    asyncio.run(load_data_to_queue())
def get_acft_data_queue(): #easy fn to load current flight queue
    return acft_data_queue