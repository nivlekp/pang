import numpy as np

import pang


def test_Sequence_simulate_queue_00():
    instances = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
    )
    sequence_duration = 10
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
        sequence_duration=sequence_duration,
    )

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


def test_Sequence_simulate_queue_01():
    instances = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    durations = [2.1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
    )
    sequence_duration = 10
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
        sequence_duration=sequence_duration,
    )

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


def test_Sequence_simulate_queue_02():
    instances = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
    )
    sequence_duration = 10
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
        sequence_duration=sequence_duration,
    )

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


def test_Sequence_simulate_queue_03():
    instances = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    durations = [2.1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
    )
    sequence_duration = 10
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
        sequence_duration=sequence_duration,
    )

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


def test_Sequence_simulate_queue_04():
    instances = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
    durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
    )
    sequence_duration = 10
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
        sequence_duration=sequence_duration,
    )

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


def test_Sequence_simulate_queue_05():
    instances = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
    durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
    )
    sequence_duration = 10
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
        sequence_duration=sequence_duration,
        tag=10,
    )

    sequence.simulate_queue(tag_as_pitch=True)
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
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
    ]
