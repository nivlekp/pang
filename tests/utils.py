import pang


def to_sound_points(instances, durations, pitches=None):
    if pitches is None:
        pitches = tuple(() for _ in range(len(instances)))
    return [
        pang.SoundPoint(instance, duration, pitch)
        for instance, duration, pitch in zip(instances, durations, pitches)
    ]
