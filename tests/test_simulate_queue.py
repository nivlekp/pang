import numpy as np

import pang

from .utils import to_sound_points


def test_simulate_queue_00():
    instances = [0, 1, 2, 3, 4]
    durations = [0.5, 0.5, 0.5, 0.5, 0.5]
    pitches = [0, 0, 0, 0, 0]
    sequence = pang.Sequence(to_sound_points(instances, durations, pitches), 10)
    (server,) = pang.simulate_queue(sequence, (pang.NoteServer(),))
    np.testing.assert_almost_equal(server.durations, [0.5] * (len(durations) * 2 - 1))
    assert server.pitches == [0, None, 0, None, 0, None, 0, None, 0]


def test_simulate_queue_01():
    instances = [0, 1, 2, 3, 4]
    durations = [2.1, 0.5, 0.5, 0.5, 0.5]
    pitches = [0, 0, 0, 0, 0]
    sequence = pang.Sequence(to_sound_points(instances, durations, pitches), 10)

    (server,) = pang.simulate_queue(sequence, (pang.NoteServer(),))
    np.testing.assert_almost_equal(
        server.durations,
        [2.1, 0.5, 0.5, 0.5, 0.4, 0.5],
    )

    assert server.pitches == [0, 0, 0, 0, None, 0]


def test_simulate_queue_02():
    instances = [1, 2, 3, 4]
    durations = [0.5, 0.5, 0.5, 0.5]
    pitches = [0, 0, 0, 0]
    sequence = pang.Sequence(to_sound_points(instances, durations, pitches), 5)

    (server,) = pang.simulate_queue(sequence, (pang.NoteServer(),))

    np.testing.assert_almost_equal(
        server.durations,
        [1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    )
    assert server.pitches == [None, 0, None, 0, None, 0, None, 0]


def test_simulate_queue_03():
    instances = [1, 2, 3, 4, 5]
    durations = [2.1, 0.5, 0.5, 0.5, 0.5]
    pitches = [0, 0, 0, 0, 0]
    sequence = pang.Sequence(to_sound_points(instances, durations, pitches), 6)

    (server,) = pang.simulate_queue(sequence, (pang.NoteServer(),))
    np.testing.assert_almost_equal(
        server.durations,
        [1, 2.1, 0.5, 0.5, 0.5, 0.4, 0.5],
    )

    assert server.pitches == [None, 0, 0, 0, 0, None, 0]


def test_simulate_queue_04():
    instances = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
    durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    pitches = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sequence = pang.Sequence(to_sound_points(instances, durations, pitches), 10)

    (server,) = pang.simulate_queue(sequence, (pang.NoteServer(),))
    np.testing.assert_almost_equal(
        server.durations,
        [1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    )

    assert server.pitches == [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
