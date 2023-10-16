import random

import pytest

from crunch.eyetracker.handler import DataHandler


@pytest.fixture(scope="module")
def fixation_fixture():
    def _fixation_fixture_factory(index):
        init = [111, 309, 467, 809, 1308, 1609, 1927, 2088, 2267, 2670, 2967, 3447]
        end = [203, 399, 539, 1219, 1499, 1701, 2044, 2239, 2358, 2940, 3142, 3675]
        fy = [720, 672, 653, 599, 621, 664, 566, 636, 652, 792, 810, 663]
        fx = [1054, 1166, 1087, 1052, 1048, 1069, 717, 856, 821, 527, 559, 938]
        return {
            "initTime": init[index % 12],
            "endTime": end[index % 12],
            "fx": fx[index % 12],
            "fy": fy[index % 12],
        }

    return _fixation_fixture_factory


@pytest.fixture(scope="module")
def gaze_point_fixture():
    def _gaze_fixture_factory():
        return {"lpup": random.uniform(3, 4), "rpup": random.uniform(3, 4)}

    return _gaze_fixture_factory


@pytest.mark.parametrize("window, baseline", [(2, 2), (2, 3), (5, 5), (2, 10)])
def test_gaze_handler(gaze_point_fixture, window, baseline):
    """Test that the handler uses data points for baseline
    until it has received enough, and the use them for measurement"""
    handler = DataHandler(
        measurement_func=lambda lpup, rpup: 1,
        subscribed_to=["lpup", "rpup"],
        window_length=window,
        window_step=window,
        baseline_length=baseline,
    )

    for i in range(window * baseline):
        assert handler.baseline == 0
        assert handler.phase_func == handler.baseline_phase
        handler.add_data_point(gaze_point_fixture())

    assert handler.baseline != 0
    assert handler.phase_func == handler.csv_phase


@pytest.mark.parametrize("window, baseline", [(2, 2), (2, 3), (5, 5), (2, 10)])
def test_fixation_handler(fixation_fixture, window, baseline):
    """Test that the handler uses data points for baseline
    until it has received enough, and the use them for measurement"""
    handler = DataHandler(
        measurement_func=lambda initTime, endTime, fx, fy: 1,
        subscribed_to=["initTime", "endTime", "fx", "fy"],
        window_length=window,
        window_step=window,
        baseline_length=baseline,
    )

    for i in range(window * baseline):
        assert handler.baseline == 0
        assert handler.phase_func == handler.baseline_phase
        handler.add_data_point(fixation_fixture(i))

    assert handler.baseline != 0
    assert handler.phase_func == handler.csv_phase
