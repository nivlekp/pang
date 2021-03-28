from .soundpointsgenerators import SoundPoint


class Indicator:
    """
    Indicator base class. This is to support attaching indicators before
    quantizing using Nauert.
    """

    def __init__(self):
        pass


class Harmonics(Indicator):
    """
    Encoding Harmonics.
    """

    def __init__(self):
        pass

    @property
    def id(self):
        return 1000


def attach(indicator, event):
    r"""
    Attaching an indicator to an event.

    ..  container:: example

        >>> instances = [0, 1, 2, 3]
        >>> durations = [1, 1, 0.5, 0.5]
        >>> sound_points_generator = pang.ManualSoundPointsGenerator(
        ...     instances=instances,
        ...     durations=durations,
        ... )
        >>> sequence = pang.Sequence(
        ...     sound_points_generator=sound_points_generator,
        ... )
        >>> for event in sequence:
        ...     harmonics = pang.Harmonics()
        ...     pang.attach(harmonics, event)
        ...
        >>> print(sequence.pitches)
        [(0, 1000), (0, 1000), (0, 1000), (0, 1000)]

    """
    assert isinstance(indicator, Indicator)
    assert isinstance(event, SoundPoint)
    event.pitch = (event.pitch, indicator.id)
