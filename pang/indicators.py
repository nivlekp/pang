import enum

import abjad

from .soundpointsgenerators import SoundPoint


@enum.unique
class IndicatorID(enum.Enum):
    HARMONICS = 1000


class Indicator:
    """
    Indicator base class. This is to support attaching indicators before
    quantizing using Nauert.
    """

    def __init__(self):
        pass


class Harmonics(Indicator):
    r"""
    Encoding and attaching harmonics.

    ..  container:: example

        >>> instances = [0, 1, 2, 3]
        >>> durations = [1, 1, 0.5, 0.5]
        >>> pitches = [0, 0, (0, 12), 0]
        >>> sound_points_generator = pang.ManualSoundPointsGenerator(
        ...     instances=instances,
        ...     durations=durations,
        ...     pitches=pitches,
        ... )
        >>> sequence = pang.Sequence(
        ...     sound_points_generator=sound_points_generator,
        ... )
        >>> for event in sequence:
        ...     harmonics = pang.Harmonics()
        ...     pang.attach(harmonics, event)
        ...
        >>> sequence.simulate_queue()
        >>> server = sequence.servers[0]
        >>> q_event_sequence = server.q_event_sequence
        >>> quantizer = nauert.Quantizer()
        >>> optimizer = nauert.MeasurewiseAttackPointOptimizer()
        >>> result = quantizer(q_event_sequence, attack_point_optimizer=optimizer)
        >>> pang.decode(result)
        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            \new Voice
            {
                {
                    \tweak NoteHead.style #'harmonic
                    c'4
                    \tweak NoteHead.style #'harmonic
                    c'4
                    <
                        c'
                        \tweak NoteHead.style #'harmonic
                        c''
                    >8
                    r8
                    \tweak NoteHead.style #'harmonic
                    c'8
                    r8
                }
            }
    """

    def __init__(self):
        pass

    def __call__(self, client):
        if isinstance(client, abjad.Chord):
            target = client.note_heads[-1]
        else:
            assert isinstance(client, abjad.Note)
            target = client.note_head
        abjad.tweak(target).NoteHead.style = "#'harmonic"

    @property
    def id(self):
        return IndicatorID.HARMONICS.value


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
    if isinstance(event.pitch, int):
        pitch_list = [event.pitch]
    else:
        pitch_list = list(event.pitch)
    pitch_list.append(indicator.id)
    event.pitch = tuple(pitch_list)


def decode_one_leaf(leaf):
    assert isinstance(leaf, abjad.Leaf)
    effective_pitches = []
    indicators = []
    for pitch in abjad.iterate(leaf).pitches():
        if pitch.number == IndicatorID.HARMONICS.value:
            indicators.append(Harmonics())
        else:
            effective_pitches.append(pitch)
    if indicators != []:
        if len(effective_pitches) == 1:
            new_leaf = abjad.Note.from_pitch_and_duration(
                effective_pitches[0], leaf.written_duration
            )
        else:
            new_leaf = abjad.Chord(tuple(effective_pitches), leaf.written_duration)
        for indicator in indicators:
            indicator(new_leaf)
        abjad.mutate.replace(leaf, new_leaf)


def decode(client):
    for leaf in abjad.iterate(client).leaves():
        decode_one_leaf(leaf)
