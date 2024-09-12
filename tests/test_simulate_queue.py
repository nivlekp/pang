import numpy as np
import pytest

import pang

from .utils import to_sound_points


class SingleNoteServer0(pang.NoteServer):
    def can_serve(self, sound_point: pang.SoundPoint) -> bool:
        return sound_point.pitch == 0


class SingleNoteServer1(pang.NoteServer):
    def can_serve(self, sound_point: pang.SoundPoint) -> bool:
        return sound_point.pitch == 1


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


def test_simulate_queue_with_two_servers_but_allocated_to_one_only():
    instances = [0, 1, 2, 3, 4]
    durations = [0.5, 0.5, 0.5, 0.5, 0.5]
    pitches = [0, 0, 0, 0, 0]
    sequence = pang.Sequence(to_sound_points(instances, durations, pitches), 10)
    server0, server1 = pang.simulate_queue(
        sequence, (pang.NoteServer(), pang.NoteServer())
    )
    np.testing.assert_almost_equal(server0.durations, [0.5] * (len(durations) * 2 - 1))
    assert server0.pitches == [0, None, 0, None, 0, None, 0, None, 0]
    assert server1.durations == []
    assert server1.pitches == []


def test_simulate_queue_with_two_servers_alternating():
    instances = [0, 1, 2, 3, 4]
    durations = [1.5, 1.5, 1.5, 1.5, 1.5]
    pitches = [0, 1, 0, 1, 0]
    sequence = pang.Sequence(to_sound_points(instances, durations, pitches), 10)
    server0, server1 = pang.simulate_queue(
        sequence, (pang.NoteServer(), pang.NoteServer())
    )
    np.testing.assert_almost_equal(server0.durations, [1.5, 0.5, 1.5, 0.5, 1.5])
    assert server0.pitches == [0, None, 0, None, 0]
    np.testing.assert_almost_equal(server1.durations, [1.0, 1.5, 0.5, 1.5])
    assert server1.pitches == [None, 1, None, 1]


def test_simulate_queue_with_two_servers_serving_non_overlapping_pitches():
    instances = [0, 1, 2, 3, 4]
    durations = [0.5, 0.5, 0.5, 0.5, 0.5]
    pitches = [0, 1, 0, 1, 0]
    sequence = pang.Sequence(to_sound_points(instances, durations, pitches), 10)
    server0, server1 = pang.simulate_queue(
        sequence, (SingleNoteServer0(), SingleNoteServer1())
    )
    np.testing.assert_almost_equal(server0.durations, [0.5, 1.5, 0.5, 1.5, 0.5])
    assert server0.pitches == [0, None, 0, None, 0]
    np.testing.assert_almost_equal(server1.durations, [1.0, 0.5, 1.5, 0.5])
    assert server1.pitches == [None, 1, None, 1]


def test_simulate_queue_with_two_servers_out_of_order_serving():
    instances = [0, 1, 2, 3]
    durations = [2.5, 0.5, 0.5, 0.5]
    pitches = [0, 0, 1, 1]
    sequence = pang.Sequence(to_sound_points(instances, durations, pitches), 10)
    server0, server1 = pang.simulate_queue(
        sequence, (SingleNoteServer0(), SingleNoteServer1())
    )
    np.testing.assert_almost_equal(server0.durations, [2.5, 0.5])
    assert server0.pitches == [0, 0]
    np.testing.assert_almost_equal(server1.durations, [2.0, 0.5, 0.5, 0.5])
    assert server1.pitches == [None, 1, None, 1]


def test_simulate_queue_raises_exception_if_non_servable_sound_point_exists():
    instances = [0, 1]
    durations = [1, 1]
    pitches = [0, 1]
    sequence = pang.Sequence(to_sound_points(instances, durations, pitches), 10)
    with pytest.raises(pang.NotServableException):
        pang.simulate_queue(sequence, (SingleNoteServer0(),))
