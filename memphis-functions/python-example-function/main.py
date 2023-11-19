import json
import base64
from memphis.functions import create_function

def handler(event, context): # The name of this function should match the handler field in the memphis.yaml file
    return create_function(event, event_handler = event_handler)

def event_handler(msg_payload, msg_headers, inputs):
    """
    Parameters:
    - msg_payload (bytes): The byte object representing the message payload.
    - msg_headers (dict): A dictionary containing message headers.
    - inputs (dict): A dictionary containing inputs related to the event.

    Returns:
    ((bytes), dict)
    """
    # Here is a short example of converting the message to a dict and then back to bytes
    payload =  str(msg_payload, 'utf-8')
    as_json = json.loads(payload)
    
    # Modify the message here

    return bytes(json.dumps(as_json), encoding='utf-8'), msg_headers