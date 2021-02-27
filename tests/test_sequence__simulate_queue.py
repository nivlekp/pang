import numpy as np

import pang


def test_sequencesimulate_queue_00():
    arrival_rate = 1
    service_rate = 2
    sequence_duration = 10
    sequence = pang.AtaxicCloud(
        arrival_rate=arrival_rate,
        service_rate=service_rate,
        sequence_duration=sequence_duration,
        queue_type="M/M/1",
        rest_threshold=0.0,
    )

    number_of_notes = sequence.number_of_notes
    assert number_of_notes == sequence_duration * arrival_rate

    sequence._instances = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    sequence._durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    sequence.simulate_queue()
    np.testing.assert_almost_equal(
        sequence.servers[0].durations,
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

    assert sequence.servers[0].pitches == [
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


def test_sequencesimulate_queue_01():
    arrival_rate = 1
    service_rate = 2
    sequence_duration = 10
    sequence = pang.AtaxicCloud(
        arrival_rate=arrival_rate,
        service_rate=service_rate,
        sequence_duration=sequence_duration,
        queue_type="M/M/1",
        rest_threshold=0.0,
    )

    number_of_notes = sequence.number_of_notes
    assert number_of_notes == sequence_duration * arrival_rate

    sequence._instances = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    sequence._durations = [2.1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    sequence.simulate_queue()
    np.testing.assert_almost_equal(
        sequence.servers[0].durations,
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

    assert sequence.servers[0].pitches == [
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


def test_sequencesimulate_queue_02():
    arrival_rate = 1
    service_rate = 2
    sequence_duration = 10
    sequence = pang.AtaxicCloud(
        arrival_rate=arrival_rate,
        service_rate=service_rate,
        sequence_duration=sequence_duration,
        queue_type="M/M/1",
        rest_threshold=0.0,
    )

    number_of_notes = sequence.number_of_notes
    assert number_of_notes == sequence_duration * arrival_rate

    sequence._instances = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sequence._durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    assert len(sequence.instances) == len(sequence.durations)
    sequence.simulate_queue()
    np.testing.assert_almost_equal(
        sequence.servers[0].durations,
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

    assert sequence.servers[0].pitches == [
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


def test_sequencesimulate_queue_03():
    arrival_rate = 1
    service_rate = 2
    sequence_duration = 10
    sequence = pang.AtaxicCloud(
        arrival_rate=arrival_rate,
        service_rate=service_rate,
        sequence_duration=sequence_duration,
        queue_type="M/M/1",
        rest_threshold=0.0,
    )

    number_of_notes = sequence.number_of_notes
    assert number_of_notes == sequence_duration * arrival_rate

    sequence._instances = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sequence._durations = [2.1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    assert len(sequence.instances) == len(sequence.durations)
    sequence.simulate_queue()
    np.testing.assert_almost_equal(
        sequence.servers[0].durations,
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

    assert sequence.servers[0].pitches == [
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


def test_sequencesimulate_queue_04():
    arrival_rate = 1
    service_rate = 2
    sequence_duration = 10
    sequence = pang.AtaxicCloud(
        arrival_rate=arrival_rate,
        service_rate=service_rate,
        sequence_duration=sequence_duration,
        queue_type="M/M/1",
        rest_threshold=0.0,
    )

    number_of_notes = sequence.number_of_notes
    assert number_of_notes == sequence_duration * arrival_rate

    sequence._instances = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
    sequence._durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    assert len(sequence.instances) == len(sequence.durations)
    sequence.simulate_queue()
    np.testing.assert_almost_equal(
        sequence.servers[0].durations,
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

    assert sequence.servers[0].pitches == [
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
