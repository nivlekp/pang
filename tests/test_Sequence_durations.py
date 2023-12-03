import pang


def test_ManualSequence_durations_01():
    instances = [0, 1, 2, 3]
    durations = [0.5, 0.5, 0.5, 0.5]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
    )
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
        sequence_duration=4,
    )
    assert sequence.instances == [0, 1, 2, 3]
    assert sequence.durations == [0.5, 0.5, 0.5, 0.5]
    sequence.durations = [1, 1, 1, 1]
    assert sequence.instances == [0, 1, 2, 3]
    assert sequence.durations == [1, 1, 1, 1]
