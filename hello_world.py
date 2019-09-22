# This attempts to be (more or less) the simplest possible hello world Alexa skill.
# I've used this program as a way to practice making a very basic Alexa skill.
# It is based on this blog post,
# https://www.hackster.io/auctoris/simple-python-hello-world-with-alexa-4308e4


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

    card_title = 'Hello World app'
    speech_output = '<speak>This is Hello World.</speak>'
    card_output = 'This is Hello World.'
    return build_response(session_attributes={},
                          speech_response=build_speech_response(title=card_title,
                                                                ssml_output=speech_output,
                                                                plain_output=card_output))
