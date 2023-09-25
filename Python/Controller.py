import json
import numpy as np
import tobii_research as tr
from CognitiveLoad import compute_cognitive_load
from math import isnan
from SimpleARIMAForecasting import establish_reference, predict_next_direction
import requests

found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)


valid_lpup = [0.5]
valid_rpup = [0.5]
baseline = [0, 0]
cognitive_load_array = []


def callback(gaze_data):
    """
    Callback function used by the Tobii Pro SDK when the eyetracker provides an update
    Parameters:
    - gaze_data: Data from the eyetracker
    """

    lpup = gaze_data["left_pupil_diameter"]
    rpup = gaze_data["right_pupil_diameter"]

    """If pupil data is invalid, use other valid pupil or the previous valid pupil data"""
    if isnan(lpup) and isnan(rpup):
        valid_lpup.append(valid_lpup[-1])
        valid_rpup.append(valid_rpup[-1])
    elif isnan(lpup) and not isnan(rpup):
        valid_lpup.append(rpup)
        valid_rpup.append(rpup)
    elif not isnan(lpup) and isnan(rpup):
        valid_lpup.append(lpup)
        valid_rpup.append(lpup)
    else:
        valid_lpup.append(lpup)
        valid_rpup.append(rpup)

    cognitive_load = compute_cognitive_load(valid_lpup, valid_rpup)
    if cognitive_load:  # Don't append cogntive load if it is measured to 0
        cognitive_load_array.append(cognitive_load)
    if len(cognitive_load_array) == 500:  # Establish baseline
        baseline[0], baseline[1] = establish_reference(cognitive_load_array)
    if (
        len(cognitive_load_array) % 500 == 0
        and len(cognitive_load_array) != 0
        and len(cognitive_load_array) != 500
    ):  # Make forecast every 500 eytracker update
        prediction = predict_next_direction(cognitive_load_array[-500:], baseline[0], baseline[1])
        if prediction == "up":
            # Ping the server when prediction is "up"
            headers = {'Content-Type': 'application/json'}
            response = requests.post("http://127.0.0.1:8080/get_data", headers=headers, data=json.dumps({"direction": prediction}))
            print(response.json()["response"])

    # Send the data to Flask server
    new_data_chunk = np.random.rand(90)
    payload = {
        'pupil_size': (valid_lpup[-1] + valid_rpup[-1]) / 2,
        'cognitive_load': new_data_chunk
    }
    try:
        response = requests.post('http://localhost:8080/update_data', json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors.
    except requests.RequestException as error:
        print(f"Failed to send data to Flask server: {error}")



my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, callback, as_dictionary=True)


while True:
    pass
