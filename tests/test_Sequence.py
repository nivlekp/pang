import pang


def test_Sequence_from_sound_point_generator():
    instances = [0, 1, 2, 3]
    durations = [0.5, 0.5, 0.5, 0.5]
    pitches = [0, 0, 0, 0]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
        pitches=pitches,
    )
    sequence = pang.Sequence.from_sound_point_generator(
        sound_points_generator=sound_points_generator, sequence_duration=0
    )
    assert sequence.instances == instances
    assert sequence.durations == durations
    assert sequence.pitches == pitches
    assert sequence.sequence_duration == 3.5
