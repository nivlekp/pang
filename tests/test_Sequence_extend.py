import pang


def test_ManualSequence_extend_01():
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
    sequence_1 = pang.Sequence(
        sound_points_generator=sound_points_generator,
    )
    sequence_0.extend(sequence_1)
    assert sequence_0.instances == [0, 1, 2, 3, 4, 5, 6, 7]
    assert sequence_0.durations == [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    assert sequence_0.pitches == [0, 0, 0, 0, 0, 0, 0, 0]
