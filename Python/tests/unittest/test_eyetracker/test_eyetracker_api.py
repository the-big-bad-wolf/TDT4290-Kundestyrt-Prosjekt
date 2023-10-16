import pytest

from crunch.eyetracker.api import EyetrackerAPI


class MockSubscriber:
    """ Mock subscriber to test that we receive data points from the api """
    nr_points_received = 0

    def add_data_point(self, _):
        self.nr_points_received += 1


@pytest.fixture(scope="module")
def raw_gaze_fixture():
    def _gaze_fixture_factory(index, move_left=0):
        return {
            'device_time_stamp': 312133244857 + index*100000/120,
            'left_pupil_diameter': 0.5,
            'left_gaze_point_on_display_area': (0.753740668296814 - move_left, -0.11630667001008987),
            'right_gaze_point_on_display_area': (1.1366922855377197 - move_left, -0.03179898485541344),
            'right_pupil_diameter': 0.4
        }
    return _gaze_fixture_factory


@pytest.mark.parametrize('expected', [1, 5, 10, 50])
def test_gaze(raw_gaze_fixture, expected):
    """ Test that the api sends the gaze data that it receives to its subscribers """
    mock_subscriber = MockSubscriber()
    api = EyetrackerAPI()
    api.add_subscriber(mock_subscriber, "gaze")
    for i in range(expected):
        api.gaze_data_callback(raw_gaze_fixture(i))

    assert mock_subscriber.nr_points_received == expected


@pytest.mark.parametrize('expected, move_gaze_index', [(0, []), (1, [5]), (5, [5, 10, 20, 30, 40])])
def test_fixation(raw_gaze_fixture, expected, move_gaze_index):
    """ Test that the api sends the fixation data when a fixation occurs """
    mock_subscriber = MockSubscriber()
    api = EyetrackerAPI()
    api.add_subscriber(mock_subscriber, "fixation")
    move_eye_left = 0
    for i in range(100):
        if i in move_gaze_index:
            move_eye_left += 3
        api.gaze_data_callback(raw_gaze_fixture(i, move_eye_left))

    assert mock_subscriber.nr_points_received == expected
