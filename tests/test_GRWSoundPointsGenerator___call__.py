import pang


def test_GRWSoundPointsGenerator___call___01():
    pitch_set = list(range(48))
    sound_points_generator = pang.GRWSoundPointsGenerator(
        pitch_set=pitch_set,
        standard_deviation=2,
    )
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
        sequence_duration=10,
    )
    sequence.simulate_queue()
    assert sequence.servers[0].pitches == [
        None,
        24,
        23,
        None,
        24,
        None,
        25,
        23,
        22,
        22,
        None,
        19,
        20,
        21,
    ]
