import pytest

import pang

from .utils import to_sound_points


def test_Sequence_with_out_of_order_sound_points_raises_exception():
    with pytest.raises(ValueError) as exception_info:
        pang.Sequence(to_sound_points([1, 0], [1, 1]), 2)
    assert "out of order" in str(exception_info.value)


def test_Sequence_with_strictly_overtime_sound_point_raises_exception():
    with pytest.raises(ValueError) as exception_info:
        pang.Sequence(to_sound_points([0, 3], [1, 1]), 2)
    assert "The last sound point starts after the sequence ended" in str(
        exception_info.value
    )


def test_Sequence_insert():
    sequence_0 = pang.Sequence(
        to_sound_points([0, 1, 2, 3], [0.5, 0.5, 0.5, 0.5], [0, 0, 0, 0]), 4
    )
    sequence_1 = pang.Sequence(
        to_sound_points([0, 1, 2, 3], [0.5, 0.5, 0.5, 0.5], [1, 1, 1, 1]), 4
    )
    sequence_0.insert(2, sequence_1)
    assert sequence_0.instances == [0, 1, 2, 3, 4, 5, 6, 7]
    assert sequence_0.pitches == [0, 0, 1, 1, 1, 1, 0, 0]
    assert sequence_0.durations == [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]


def test_Sequence_insert_overtime_sequence():
    sequence_0 = pang.Sequence(
        to_sound_points([0, 1, 2, 3], [0.5, 0.5, 0.5, 0.5], [0, 0, 0, 0]), 4
    )
    sequence_1 = pang.Sequence(
        to_sound_points([0, 1, 2, 3], [0.5, 0.5, 0.5, 1.5], [1, 1, 1, 1]), 4
    )
    sequence_0.insert(2, sequence_1)
    assert sequence_0.instances == [0, 1, 2, 3, 4, 5, 6, 7]
    assert sequence_0.pitches == [0, 0, 1, 1, 1, 1, 0, 0]
    assert sequence_0.durations == [0.5, 0.5, 0.5, 0.5, 0.5, 1.5, 0.5, 0.5]


def test_Sequence_extend_by_itself():
    sequence = pang.Sequence(to_sound_points([0, 1, 2, 3], [0.5, 0.5, 0.5, 0.5]), 4)
    sequence.extend(sequence)
    assert sequence.instances == [0, 1, 2, 3, 4, 5, 6, 7]
    assert all(duration == 0.5 for duration in sequence.durations)
    assert all(pitch == () for pitch in sequence.pitches)


def test_Sequence_extend_with_overtime_sequence():
    sequence_0 = pang.Sequence(
        to_sound_points([0, 1, 2, 3], [0.5, 0.5, 0.5, 1.5], [0, 0, 0, 0]), 4
    )
    sequence_1 = pang.Sequence(
        to_sound_points([0, 1, 2, 3], [0.5, 0.5, 0.5, 0.5], [1, 1, 1, 1]), 4
    )
    sequence_0.extend(sequence_1)
    assert sequence_0.instances == [0, 1, 2, 3, 4, 5, 6, 7]
    assert sequence_0.pitches == [0, 0, 0, 0, 1, 1, 1, 1]
    assert sequence_0.durations == [0.5, 0.5, 0.5, 1.5, 0.5, 0.5, 0.5, 0.5]


def test_Sequence_superpose():
    sequence_0 = pang.Sequence(
        to_sound_points([0, 1, 2, 3], [0.5, 0.5, 0.5, 0.5], [0, 0, 0, 0]), 4
    )

    sequence_1 = pang.Sequence(
        to_sound_points([0.5, 1.5, 2.5, 3.5], [0.6, 0.6, 0.7, 0.7], [1, 1, 1, 1]), 4.5
    )
    sequence_0.superpose(0, sequence_1)
    assert sequence_0.instances == [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
    assert sequence_0.durations == [0.5, 0.6, 0.5, 0.6, 0.5, 0.7, 0.5, 0.7]
    assert sequence_0.pitches == [0, 1, 0, 1, 0, 1, 0, 1]


def test_Sequence_from_sound_points_generator():
    instances = [0, 1, 2, 3]
    durations = [0.5, 0.5, 0.5, 0.5]
    pitches = [0, 0, 0, 0]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
        pitches=pitches,
    )
    sequence = pang.Sequence.from_sound_points_generator(
        sound_points_generator=sound_points_generator, sequence_duration=4
    )
    assert sequence.instances == instances
    assert sequence.durations == durations
    assert sequence.pitches == pitches
    assert sequence.sequence_duration == 4


def test_Sequence_from_sequences():
    sequence_0 = pang.Sequence(
        to_sound_points([0, 1, 2, 3], [0.5, 0.5, 0.5, 0.5], [0, 0, 0, 0]), 4
    )
    sequence_1 = pang.Sequence(
        to_sound_points([0, 1, 2, 3], [0.6, 0.6, 0.6, 0.6], [1, 1, 1, 1]), 4
    )
    sequence_2 = pang.Sequence(
        to_sound_points([0, 1, 2, 3], [0.7, 0.7, 0.7, 0.7], [2, 2, 2, 2]), 4
    )
    sequence = pang.Sequence.from_sequences([sequence_0, sequence_1, sequence_2])
    assert sequence.instances == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    assert sequence.pitches == [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
    assert sequence.durations == [
        0.5,
        0.5,
        0.5,
        0.5,
        0.6,
        0.6,
        0.6,
        0.6,
        0.7,
        0.7,
        0.7,
        0.7,
    ]
    assert sequence.sequence_duration == 12


def test_Sequence_empty_sequence():
    assert pang.Sequence.empty_sequence() == pang.Sequence([], 0)


def test_Sequence___eq__():
    assert pang.Sequence([], 0) == pang.Sequence([], 0)
    assert pang.Sequence([], 0) != pang.Sequence([], 1)
    assert pang.Sequence(to_sound_points([0, 1], [1, 1]), 2) != pang.Sequence([], 2)
