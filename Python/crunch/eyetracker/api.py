import time
from math import isnan


class GazedataToFixationdata:
    """
    Class that takes in gaze data points from the EyetrackerAPI, preprocesses the gaze points,
     and computes fixation_data.

     The class attribute velocity_threshold is very important and determines how sensitive
     the class is to eyemovement. The higher the value is, the more gaze points will be
     classified as part of a fixation. The value 0.05 was set based on 10 minutes of
     experimentation, but should probably be adjusted.

    RealAPI calls insert_new_gaze_data, the rest is helper functions.
    For more information on gaze data and fixation data, see:
    https://www.tobiipro.com/learn-and-support/learn/eye-tracking-essentials/types-of-eye-movements/
    """
    list_of_gaze_data_points_in_a_fixation = []
    last_gaze_data_point = None
    last_velocity_was_fixation = None

    screen_proportions = (1920, 1080)
    velocity_threshold = 0.05
    first_time_stamp = None

    def insert_new_gaze_data(self, left_eye_fx, left_eye_fy, right_eye_fx, right_eye_fy, timestamp):
        """
        Called from RealAPI. Preprocesses the gaze data and classifies the gaze point
        as part of a saccade or a part of a fixation by checking if  velocity is
        above or below the threshold.
        The condition for returning a fixation point is that:
            1. At least the 2 previous gaze points had low velocity (part of a fixation)
            2. The current gaze point has high velocity (part of a saccade)

        All parameters are float, but can be nan.
        return: fixation point or None
        """
        fixation_point = None
        fx = self.preprocess_eyetracker_gazepoint(left_eye_fx, right_eye_fx, is_fx=True) * self.screen_proportions[0]
        fy = self.preprocess_eyetracker_gazepoint(left_eye_fy, right_eye_fy, is_fx=False) * self.screen_proportions[1]

        if self.last_gaze_data_point is not None:
            velocity = self.velocity(fx, fy, timestamp, self.last_gaze_data_point['fx'],
                                     self.last_gaze_data_point['fy'],
                                     self.last_gaze_data_point['timestamp'])

            # Check if this is a saccade
            if velocity > self.velocity_threshold:
                # check if last
                if self.last_velocity_was_fixation and len(self.list_of_gaze_data_points_in_a_fixation) > 2:
                    fixation_point = self.end_fixation()
                self.last_velocity_was_fixation = False

            # If not a saccade, this is a fixation
            else:
                self.last_velocity_was_fixation = True
                self.list_of_gaze_data_points_in_a_fixation.append({"fx": fx, "fy": fy, "timestamp": timestamp})

        self.last_gaze_data_point = {"fx": fx, "fy": fy, "timestamp": timestamp}
        if self.first_time_stamp is None:
            self.first_time_stamp = timestamp

        return fixation_point

    def end_fixation(self):
        """Ends the fixation by setting initTime, endTime, fx and fy"""
        number_of_gazepoints = len(self.list_of_gaze_data_points_in_a_fixation)

        initTime = (self.list_of_gaze_data_points_in_a_fixation[0]["timestamp"] - self.first_time_stamp) / 1000
        endTime = (self.list_of_gaze_data_points_in_a_fixation[-1]["timestamp"] - self.first_time_stamp) / 1000
        fx = sum(gazepoint['fx'] for gazepoint in self.list_of_gaze_data_points_in_a_fixation) / number_of_gazepoints
        fy = sum(gazepoint['fy'] for gazepoint in self.list_of_gaze_data_points_in_a_fixation) / number_of_gazepoints
        fixation_point = {"initTime": initTime, "endTime": endTime, "fx": fx, "fy": fy}
        self.list_of_gaze_data_points_in_a_fixation = []

        return fixation_point

    def distance(self, fx1, fy1, fx2, fy2):
        """returns euclidean distance"""
        return ((fx1 - fx2) ** 2 + (fy1 - fy2) ** 2) ** 0.5

    def velocity(self, fx1, fy1, timestamp1, fx2, fy2, timestamp2):
        """Velocity measures how fast the eyes move from gazepoint 1 to gazepoint 2. euclidean distance/time"""
        return self.distance(fx1, fy1, fx2, fy2) / (abs(timestamp2 - timestamp1))

    def preprocess_eyetracker_gazepoint(self, left_eye_fx_or_fy, right_eye_fx_or_fy, is_fx=True):
        """
        Takes in either a left and a right fx value, or a left and a right fy value

        :return fx or fy: average of the left and right eye coordinate
        :type fx or fy: float
        """
        if isnan(left_eye_fx_or_fy) and isnan(right_eye_fx_or_fy):
            if is_fx and self.last_gaze_data_point is not None:
                return self.last_gaze_data_point["fx"]
            elif not is_fx and self.last_gaze_data_point is not None:
                return self.last_gaze_data_point["fy"]
            else:
                return 0

        elif isnan(left_eye_fx_or_fy):
            left_eye_fx_or_fy = right_eye_fx_or_fy
        elif isnan(right_eye_fx_or_fy):
            right_eye_fx_or_fy = left_eye_fx_or_fy
        return (left_eye_fx_or_fy + right_eye_fx_or_fy) / 2


class EyetrackerAPI:
    """
    Responsible for connecting to and receiving gaze data from the eyetracker,
    and then the API sends the data to all handlers that are subscribed.

    The API cleans pupil data (gaze data) which is sent to gaze subscribers.
    The API sends gaze data to GazedataToFixationdata which irregularly returns
    fixation data that is sent to fixation subscribers.
    """
    subscribers = {"gaze": [], "fixation": []}
    last_valid_pupil_data = (0.5, 0.5)

    def __init__(self):
        self.gaze_to_fixation = GazedataToFixationdata()

    def connect(self):
        """ Connect the eyetracker to the callback function """
        #  Need to import here instead of top of file because of CI
        import tobii_research as tr
        if len(tr.find_all_eyetrackers()) == 0:
            print("No eyetracker was found")
        else:
            my_eyetracker = tr.find_all_eyetrackers()[0]
            my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)
            #  For some reason we get crashes if this time.sleep is removed
            while True:
                time.sleep(15)
            # my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)

    def gaze_data_callback(self, gaze_data):
        """Callback function that the eyetracker device calls 120 times a second. Inserts data to EyetrackerAPI"""
        left_eye_fx, left_eye_fy = gaze_data['left_gaze_point_on_display_area']
        right_eye_fx, right_eye_fy = gaze_data['right_gaze_point_on_display_area']
        timestamp = gaze_data['device_time_stamp']
        lpup = gaze_data['left_pupil_diameter']
        rpup = gaze_data['right_pupil_diameter']

        # handle fixation data
        fixation_point = self.gaze_to_fixation.insert_new_gaze_data(left_eye_fx,
                                                                    left_eye_fy,
                                                                    right_eye_fx,
                                                                    right_eye_fy,
                                                                    timestamp)
        if fixation_point is not None:
            self.send_data_to_handlers("fixation", fixation_point)

        # handle gaze data
        gaze_point = self.preprocess_eyetracker_pupils(lpup, rpup)
        self.send_data_to_handlers("gaze", gaze_point)

    def preprocess_eyetracker_pupils(self, lpup, rpup):
        """If pupil data is invalid, use other valid pupil or the previous valid pupil data"""
        if isnan(lpup) and isnan(rpup):
            pass
        elif isnan(lpup) and not isnan(rpup):
            self.last_valid_pupil_data = (rpup, rpup)
        elif not isnan(lpup) and isnan(rpup):
            self.last_valid_pupil_data = (lpup, lpup)
        else:
            self.last_valid_pupil_data = (lpup, rpup)
        lpup, rpup = self.last_valid_pupil_data
        return {"lpup": lpup, "rpup": rpup}

    def send_data_to_handlers(self, name, data):
        """Send data to all handlers"""
        for handler in self.subscribers[name]:
            handler.add_data_point(data)

    def add_subscriber(self, handler, requested_data):
        """
        Adds a handler as a subscriber for a specific requested data

        :param handler: a data handler for a specific measurement that subscribes to a specific raw data
        :type handler: DataHandler
        :param requested_data: name of the requested data
        :type requested_data: str
        """
        self.subscribers[requested_data].append(handler)
