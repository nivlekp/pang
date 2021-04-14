import enum

import abjad

from .soundpointsgenerators import SoundPoint


def _attach_id_to_pitch_list(event, id_):
    if isinstance(event.pitch, (int, float)):
        pitch_list = [event.pitch]
    else:
        pitch_list = list(event.pitch)
    pitch_list.append(id_)
    return pitch_list


@enum.unique
class IndicatorID(enum.Enum):
    HARMONICS = 1000
    BLUE = 2000
    RED = 3000

    @classmethod
    def has_value(class_, value):
        return value in set(item.value for item in class_)

    @classmethod
    def get_class_name(class_, value):
        name = class_(value).name
        return name[0] + name[1:].lower()


class Indicator:
    """
    Indicator base class. This is to support attaching indicators before
    quantizing using Nauert.
    """

    def __init__(self):
        pass

    def attach(self, event):
        """
        Attach the "payload" to the event
        """
        raise NotImplementedError


class Red(Indicator):
    r"""
    Encoding and attaching the color red.

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
        ...     harmonics = pang.Red()
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
                    \tempo 4=60
                    %%% \time 4/4 %%%
                    <
                        \tweak color #red
                        c'
                    >4
                    <
                        \tweak color #red
                        c'
                    >4
                    <
                        \tweak color #red
                        c'
                        \tweak color #red
                        c''
                    >8
                    r8
                    <
                        \tweak color #red
                        c'
                    >8
                    r8
                }
            }
    """

    def __call__(self, client):
        """
        Call indicator to process the client while decoding.
        """
        for note_head in client.note_heads:
            abjad.tweak(note_head).color = "#red"

    def attach(self, event):
        """
        Attach the "payload" to the event.
        """
        pitch_list = _attach_id_to_pitch_list(event, self.id)
        event.pitch = tuple(pitch_list)

    @property
    def id(self):
        return IndicatorID.RED.value


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
                    \tempo 4=60
                    %%% \time 4/4 %%%
                    <
                        \tweak NoteHead.style #'harmonic
                        c'
                    >4
                    <
                        \tweak NoteHead.style #'harmonic
                        c'
                    >4
                    <
                        \tweak NoteHead.style #'harmonic
                        c'
                        c''
                    >8
                    r8
                    <
                        \tweak NoteHead.style #'harmonic
                        c'
                    >8
                    r8
                }
            }
    """

    def __init__(self, harmonic=None):
        self._harmonic = harmonic

    def __call__(self, client):
        """
        Call indicator to process the client while decoding.
        """
        if isinstance(client, abjad.Chord):
            target = client.note_heads[0]
        else:
            assert isinstance(client, abjad.Note)
            target = client.note_head
        abjad.tweak(target).NoteHead.style = "#'harmonic"

    def attach(self, event):
        """
        Attach the "payload" to the event.
        """
        pitch_list = _attach_id_to_pitch_list(event, self.id)
        if self._harmonic is not None:
            fundamental = pitch_list[0]
            pitch_list.append(fundamental + self._harmonic)
        event.pitch = tuple(pitch_list)

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
        ...     harmonics = pang.Harmonics(12)
        ...     pang.attach(harmonics, event)
        ...
        >>> print(sequence.pitches)
        [(0, 1000, 12), (0, 1000, 12), (0, 1000, 12), (0, 1000, 12)]

    """
    assert isinstance(indicator, Indicator)
    assert isinstance(event, SoundPoint)
    indicator.attach(event)


def decode_one_logical_tie(logical_tie):
    assert isinstance(logical_tie, abjad.LogicalTie)
    for leaf in logical_tie:
        effective_pitches = []
        indicators = []
        for pitch in abjad.iterate(leaf).pitches():
            if IndicatorID.has_value(pitch.number):
                indicator = globals()[IndicatorID.get_class_name(pitch.number)]()
                assert isinstance(indicator, Indicator)
                indicators.append(indicator)
            else:
                effective_pitches.append(pitch)
        if indicators != []:
            # TODO: make a new Leaf (not Chord) if `len(effective_pitches) == 1`
            leaf.written_pitches = effective_pitches
            for indicator in indicators:
                indicator(leaf)


def decode(client):
    for logical_tie in abjad.iterate(client).logical_ties():
        decode_one_logical_tie(logical_tie)
