from crunch.eyetracker.api import EyetrackerAPI
from crunch.eyetracker.handler import DataHandler
from crunch.eyetracker.measurements import (
                                            compute_cognitive_load,
                                            )                         


def start_eyetracker(api=EyetrackerAPI):
    """Defines the callback function, try to connect to eye tracker, create EyetrackerAPI and add handlers to api"""

    # Instantiate the api
    api = api()

    # Instantiate the cognital load data handler and subscribe to the api
    cognitive_load_handler = DataHandler(
        measurement_func=compute_cognitive_load,
        measurement_path="cognitive_load.csv",
        subscribed_to=["lpup", "rpup"],
        window_length=3000,
        window_step=1500,
        baseline_length=20
    )
    api.add_subscriber(cognitive_load_handler, "gaze")

    # start up the api
    api.connect()
