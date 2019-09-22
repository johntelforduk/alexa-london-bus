# https://api-portal.tfl.gov.uk/docs
# Specifically, Arrival predictions (countdown/trackernet) for a stop

# Bus with TFL's web UI,
# https://tfl.gov.uk/bus/stop/490014129N/wales-avenue?lineId=154

import requests                                 # For the TFL API invocations.
import json                                     # For converting returned text from JSON to Python list.


def remove_ssml_tags(parm_text:str) -> str:
    """Remove the SSML tags from parm text. The tags are surrounded by <chevrons>."""

    output_text = ''
    inside_chevrons = False
    for c in parm_text:
        if c == '<':
            inside_chevrons = True
        elif c == '>':
            inside_chevrons = False
        elif not inside_chevrons:
            output_text += c
    return output_text


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


def build_speech_response(title, ssml_output, plain_output):
    """Build a speech JSON representation of the title, output text, and end of session."""

    # In this app, the session always ends after a single response.
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': ssml_output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': plain_output
        },
        'shouldEndSession': True
    }


def build_response(session_attributes, speech_response):
    """Build the full response JSON from the speech response."""
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speech_response
    }


def lambda_handler(event, context):
    """Function called by Lambda. Output JSON returned to Alexa."""
    assert(event is not '')
    assert(context is not '')
    print('event.session.application.applicationId=' + event['session']['application']['applicationId'])

    buses = bus_arrivals(naptan_id='490014129N')
    print('buses=' + str(buses))
    speech_output = buses_to_speech(buses)
    print('speech_output=' + speech_output)
    card_output = remove_ssml_tags(speech_output)
    print('card_output=' + card_output)

    card_title = 'London Buses'
    print('card_title=' + card_title)

    return build_response(session_attributes={},
                          speech_response=build_speech_response(title=card_title,
                                                                ssml_output=speech_output,
                                                                plain_output=card_output))
