import pang


def test_Sequence_superpose_01():
    instances = [0, 1, 2, 3]
    durations = [0.5, 0.5, 0.5, 0.5]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
    )
    sequence_0 = pang.Sequence(
        sound_points_generator=sound_points_generator,
        sequence_duration=4,
    )

    instances = [0.5, 1.5, 2.5, 3.5]
    durations = [0.6, 0.6, 0.7, 0.7]
    pitches = [1, 1, 1, 1]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
        pitches=pitches,
    )
    sequence_1 = pang.Sequence(
        sound_points_generator=sound_points_generator,
    )
    sequence_0.superpose(sequence_1)
    assert sequence_0.instances == [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
    assert sequence_0.durations == [0.5, 0.6, 0.5, 0.6, 0.5, 0.7, 0.5, 0.7]
    assert sequence_0.pitches == [0, 1, 0, 1, 0, 1, 0, 1]
