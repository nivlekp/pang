import pang


def test_Sequence___init___01():
    instances = [0, 1, 2, 3]
    durations = [0.5, 0.5, 0.5, 0.5]
    pitches = [0, 0, 0, 0]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
        pitches=pitches,
    )
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
    )
    assert sequence.instances == instances
    assert sequence.durations == durations
    assert sequence.pitches == pitches
    assert sequence.sequence_duration == 3.5


def test_Sequence___init___02():
    instances = [0, 1, 2, 3]
    durations = [0.5, 0.5, 0.5, 0.5]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
    )
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
    )
    assert sequence.instances == instances
    assert sequence.durations == durations
    assert sequence.pitches == [0, 0, 0, 0]
    assert sequence.sequence_duration == 3.5
