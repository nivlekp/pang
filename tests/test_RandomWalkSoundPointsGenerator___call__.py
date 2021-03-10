import pang


def test_RandomWalkSoundPointsGenerator___call___01():
    pitch_set = list(range(48))
    sound_points_generator = pang.RandomWalkSoundPointsGenerator(
        pitch_set=pitch_set,
        seed=92379734,
    )
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
        sequence_duration=100,
    )
    sequence.simulate_queue()
    index = 0
    previous_pitch = None
    while previous_pitch is None:
        previous_pitch = sequence.servers[0].pitches[index]
        index += 1
    for pitch in sequence.servers[0].pitches[index:]:
        if pitch is not None:
            difference = pitch - previous_pitch
            if pitch == max(pitch_set) or pitch == min(pitch_set):
                assert difference == 1 or difference == -1 or difference == 0
            else:
                assert difference == 1 or difference == -1, print(previous_pitch, pitch)
            previous_pitch = pitch
