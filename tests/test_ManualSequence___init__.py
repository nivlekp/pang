import pang


def test_ManualSequence___init___01():
    instances = [0, 1, 2, 3]
    durations = [0.5, 0.5, 0.5, 0.5]
    pitches = [0, 0, 0, 0]
    sequence = pang.ManualSequence(
        instances=instances,
        durations=durations,
        pitches=pitches,
    )
    assert sequence.instances == instances
    assert sequence.durations == durations
    assert sequence.pitches == pitches
    assert sequence.sequence_duration == 3.5


def test_ManualSequence___init___02():
    instances = [0, 1, 2, 3]
    durations = [0.5, 0.5, 0.5, 0.5]
    sequence = pang.ManualSequence(
        instances=instances,
        durations=durations,
    )
    assert sequence.instances == instances
    assert sequence.durations == durations
    assert sequence.pitches == [0, 0, 0, 0]
    assert sequence.sequence_duration == 3.5
