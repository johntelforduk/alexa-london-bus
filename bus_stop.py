# https://api-portal.tfl.gov.uk/docs
# Specifically, Arrival predictions (countdown/trackernet) for a stop

# Bus with TFL's web UI,
# https://tfl.gov.uk/bus/stop/490014129N/wales-avenue?lineId=154

import requests                                 # For the TFL API invocations.
import json                                     # For converting returned text from JSON to Python list.


def bus_arrivals(naptan_id: str):
    """Use TFL API to return a list of bus arrivals at the parm bus stop. Each item in the list is a tuple of
       important info about the arrival. Buses in the list are sorted, with soonest arrival first.
       If the TFL API fails to respond then None will be returned.
       If there are no buses expected then an empty list will be returned.
    """

    arrivals_url = 'https://api.tfl.gov.uk/StopPoint/' + naptan_id + '/arrivals'

    request = requests.get(url=arrivals_url)        # Invoke the TFL API.

    if request.status_code != 200:
        return None
    else:
        request_list = json.loads(s=request.text)       # Convert JSON to list of dictionaries.

        bus_list = []

        for rl in request_list:
            exp_arrival_secs = rl.get('timeToStation')
            exp_arrival_mins = int(exp_arrival_secs / 60)
            bus_stop_name = rl.get('stationName')
            bus_number = rl.get('lineId')
            towards = rl.get('towards')

            bus_list.append((exp_arrival_secs, exp_arrival_mins, bus_stop_name, bus_number, towards))

        # Sorted by first item in each tuple, which is the number of seconds until arrival. This mean the list is sorted
        # to have the first bus which will arrival at the head of the list.
        return sorted(bus_list)


def due_mins_to_words(mins:int) -> str:
    """Convert the parm number of minutes to a due time in words."""
    if mins == 0:
        return 'now'
    elif mins == 1:
        return 'in 1 minute'
    else:
        return 'in ' + str(mins) + ' minutes'


def mins_to_words(mins:int) -> str:
    """Convert the parm number of minutes into words."""
    if mins == 0:
        return 'zero minutes'
    elif mins == 1:
        return '1 minute'
    else:
        return str(mins) + ' minutes'


def buses_to_speech(bus_list) -> str:
    if bus_list is None:
        return '<speak>Sorry, but I could not get information from' \
               + ' <say-as interpret-as="spell-out">TFL</say-as></speak>.'
    elif len(bus_list) == 0:
        return '<speak>There are no buses at the moment.</speak>'

    else:
        (_, exp_arrival_mins, bus_stop_name, bus_number, towards) = bus_list.pop(0)

        speech = '<speak>The next bus from ' \
                 + bus_stop_name \
                 + ' is the <say-as interpret-as="digits">' \
                 + str(bus_number) \
                 + '</say-as> towards ' \
                 + towards \
                 + ' due ' \
                 + due_mins_to_words(exp_arrival_mins) \
                 + '.'

        if len(bus_list) == 0:
            speech = speech + ' There are no more buses expected after that.'

        elif len(bus_list) == 1:
            (_, exp_arrival_mins, _, _, _) = bus_list.pop(0)
            speech += ' Followed by a bus in ' + mins_to_words(exp_arrival_mins) + ' from now.'

        else:
            speech += ' Followed by buses in '
            while len(bus_list) > 0:
                (_, exp_arrival_mins, _, _, _) = bus_list.pop(0)
                if len(bus_list) == 0:
                    speech += 'and ' + mins_to_words(exp_arrival_mins) + ' from now.'
                else:
                    speech += mins_to_words(exp_arrival_mins) + ', '

        speech += '</speak>'
        return speech