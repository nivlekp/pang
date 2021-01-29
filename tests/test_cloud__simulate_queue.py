import numpy as np

import pang


def test_cloud__simulate_queue_00():
    arate = 1
    srate = 2
    duration = 10
    pitches = [0]
    cloud = pang.Cloud(
        arate=arate,
        srate=srate,
        pitches=pitches,
        duration=duration,
        queue_type="M/M/1",
        rest_threshold=0.0,
    )

    number_of_notes = cloud.number_of_notes
    assert number_of_notes == duration * arate

    cloud._instances = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    cloud._durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    cloud._simulate_queue()
    np.testing.assert_almost_equal(
        cloud.durations_per_server[0],
        [
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
        ],
    )

    assert cloud.pitches_per_server[0] == [
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
    ]


def test_cloud__simulate_queue_01():
    arate = 1
    srate = 2
    duration = 10
    pitches = [0]
    cloud = pang.Cloud(
        arate=arate,
        srate=srate,
        pitches=pitches,
        duration=duration,
        queue_type="M/M/1",
        rest_threshold=0.0,
    )

    number_of_notes = cloud.number_of_notes
    assert number_of_notes == duration * arate

    cloud._instances = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    cloud._durations = [2.1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    cloud._simulate_queue()
    np.testing.assert_almost_equal(
        cloud.durations_per_server[0],
        [
            2.1,
            0.5,
            0.5,
            0.5,
            0.4,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
        ],
    )

    assert cloud.pitches_per_server[0] == [
        0,
        0,
        0,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
    ]


def test_cloud__simulate_queue_02():
    arate = 1
    srate = 2
    duration = 10
    pitches = [0]
    cloud = pang.Cloud(
        arate=arate,
        srate=srate,
        pitches=pitches,
        duration=duration,
        queue_type="M/M/1",
        rest_threshold=0.0,
    )

    number_of_notes = cloud.number_of_notes
    assert number_of_notes == duration * arate

    cloud._instances = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    cloud._durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    assert len(cloud.arrival_instances) == len(cloud.durations)
    cloud._simulate_queue()
    np.testing.assert_almost_equal(
        cloud.durations_per_server[0],
        [
            1,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
        ],
    )

    assert cloud.pitches_per_server[0] == [
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
    ]


def test_cloud__simulate_queue_03():
    arate = 1
    srate = 2
    duration = 10
    pitches = [0]
    cloud = pang.Cloud(
        arate=arate,
        srate=srate,
        pitches=pitches,
        duration=duration,
        queue_type="M/M/1",
        rest_threshold=0.0,
    )

    number_of_notes = cloud.number_of_notes
    assert number_of_notes == duration * arate

    cloud._instances = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    cloud._durations = [2.1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    assert len(cloud.arrival_instances) == len(cloud.durations)
    cloud._simulate_queue()
    np.testing.assert_almost_equal(
        cloud.durations_per_server[0],
        [
            1,
            2.1,
            0.5,
            0.5,
            0.5,
            0.4,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
        ],
    )

    assert cloud.pitches_per_server[0] == [
        None,
        0,
        0,
        0,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
        None,
        0,
    ]


def test_cloud__simulate_queue_04():
    arate = 1
    srate = 2
    duration = 10
    pitches = [0]
    cloud = pang.Cloud(
        arate=arate,
        srate=srate,
        pitches=pitches,
        duration=duration,
        queue_type="M/M/1",
        rest_threshold=0.0,
    )

    number_of_notes = cloud.number_of_notes
    assert number_of_notes == duration * arate

    cloud._instances = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
    cloud._durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    assert len(cloud.arrival_instances) == len(cloud.durations)
    cloud._simulate_queue()
    np.testing.assert_almost_equal(
        cloud.durations_per_server[0],
        [
            1,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
        ],
    )

    assert cloud.pitches_per_server[0] == [
        None,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
