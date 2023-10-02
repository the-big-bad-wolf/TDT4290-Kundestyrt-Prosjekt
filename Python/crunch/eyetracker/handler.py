from collections import deque

from crunch import util


class DataHandler:
    """
    Class that subscribes to a specific raw data stream,
    handles storing the data,
    calculating measurements from the data,
    and calculate baseline and writes to csv.

    The class has two phases:
        1. the baseline phase where measurement results are stored
        and we eventually take the average of these values as baseline.
        2. the csv_phase where the ratio of measurement results and the
        baseline is written to csv.
    """

    def __init__(self,
                 measurement_func=None,
                 measurement_path=None,
                 subscribed_to=None,
                 window_length=None,
                 window_step=None,
                 baseline_length=None,
                 calculate_baseline=True):
        """
        :param measurement_func: the function we call to compute measurements from the raw data
        :type measurement_func: (list) -> float
        :param measurement_path: path to the output csv file
        :type measurement_path: str
        :param window_length: length of the window, i.e number of data points for the function
        :type window_length: int
        :param window_step: how many steps for a new window, i.e for 6 steps,
        a new measurement is computed every 6 data points
        :type window_step: int
        :param baseline_length: How many measurement values used to calculate baseline
        :type baseline_length: int
        :param calculate_baseline: Should baseline be calculated? Skip if False
        :type calculate_baseline: bool
        """
        assert window_length and window_step and measurement_func and subscribed_to, \
            "Need to supply the required parameters"

        self.data_queues = {key: deque(maxlen=window_length) for key in subscribed_to}
        self.data_counter = 0
        self.window_step = window_step
        self.window_length = window_length
        self.measurement_func = measurement_func
        self.measurement_path = measurement_path
        self.subscribed_to = subscribed_to

        self.phase_func = self.baseline_phase if calculate_baseline else self.csv_phase
        self.calculate_baseline = calculate_baseline
        self.baseline = 0
        self.list_of_baseline_values = []
        self.baseline_length = baseline_length

    def add_data_point(self, datapoint):
        """
        This is the only function in Datahandler that is called from the API. It appends the
        values in datapoint and checks if we have enough data points to calculate to call
         phase_func. In the beginning, phase_func is set to baseline_phase.

        :param datapoint: A fixation data point
        :type datapoint: dictionary of floats
        """
        self.data_counter += 1
        for key, value in datapoint.items():
            self.data_queues[key].append(value)
        if (self.data_counter % self.window_step == 0
                and all(len(queue) == self.window_length for _, queue in self.data_queues.items())):
            self.phase_func()

    def baseline_phase(self):
        """
        Appends a value to be used for calculating the baseline, then checks if we have enough data points
        to transition to next phase.
        """
        measurement = self.measurement_func(**{key: list(queue) for key, queue in self.data_queues.items()})
        self.list_of_baseline_values.append(measurement)
        if len(self.list_of_baseline_values) >= self.baseline_length:
            self.transition_to_csv_phase()

    def transition_to_csv_phase(self):
        """Compute baseline and set phase_func to csv_phase"""
        self.baseline = float(sum(self.list_of_baseline_values) / len(self.list_of_baseline_values))
        self.phase_func = self.csv_phase
        assert 0 <= self.baseline < float('inf') and type(self.baseline) == float

    def csv_phase(self):
        """Calculate measurement and write the ratio relative to baseline to csv file"""
        measurement = self.measurement_func(**{key: list(queue) for key, queue in self.data_queues.items()})
        if self.calculate_baseline:
            measurement = round(measurement / self.baseline, 6)
        util.write_csv(self.measurement_path, [measurement])