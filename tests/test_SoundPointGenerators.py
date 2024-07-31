import pang


def test_ManualSoundPointGenerator():
    instances = [0, 1, 2, 3]
    durations = [0.5, 0.5, 0.5, 0.5]
    pitches = [0, 1, 0, 1]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
        pitches=pitches,
    )
    sound_points = sound_points_generator(sequence_duration=0)
    assert [sound_point.instance for sound_point in sound_points] == instances
    assert [sound_point.duration for sound_point in sound_points] == durations
    assert [sound_point.pitch for sound_point in sound_points] == pitches
