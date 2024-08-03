import pang

from .utils import to_sound_points


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


def test_Sequence_extend():
    sequence = pang.Sequence(to_sound_points([0, 1, 2, 3], [0.5, 0.5, 0.5, 0.5]), 4)
    sequence.extend(sequence)
    assert sequence.instances == [0, 1, 2, 3, 4, 5, 6, 7]
    assert all(duration == 0.5 for duration in sequence.durations)
    assert all(pitch == () for pitch in sequence.pitches)


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
        sound_points_generator=sound_points_generator, sequence_duration=0
    )
    assert sequence.instances == instances
    assert sequence.durations == durations
    assert sequence.pitches == pitches
    assert sequence.sequence_duration == instances[-1] + durations[-1]
