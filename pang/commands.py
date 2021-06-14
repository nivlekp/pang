import typing

import abjad
from abjadext import nauert

from .indicators import decode
from .sequences import Sequence


class Command:
    """
    Base command class. To be called by SegmentMaker.
    """

    def __call__(self, target):
        raise NotImplementedError


class ProcessQuantizedSequenceCommand(Command):
    """
    Command to process quantized sequence.
    """

    def __init__(self, sequence: Sequence):
        self._sequence = sequence

    def __call__(self, target: abjad.Voice):
        """
        Called internally by the SegmentMaker.
        """
        segments = self._segment_target_by_tag(target)
        for segment in segments:
            self._attach_pitches_to_segment(segment)

    def _attach_pitches_to_segment(self, segment: abjad.Selection):
        for logical_tie, event in zip(segment, self._sequence):
            for leaf in logical_tie:
                leaf.written_pitch = abjad.NumberedPitch(event.pitch).get_name(
                    locale="us"
                )

    def _segment_target_by_tag(
        self, target: abjad.Voice
    ) -> typing.List[abjad.Selection]:
        selection: abjad.Selection = abjad.select(target).logical_ties()
        all_tags: typing.List[int] = [
            tag for tag in self._sequence.tags if tag is not None
        ]
        unique_tags: typing.List[int] = list(set(all_tags))
        pitch_tags: typing.List[abjad.NumberedPitch] = [
            abjad.NumberedPitch(tag) for tag in unique_tags
        ]
        results: typing.List[typing.Union[abjad.Selection, abjad.Expression]] = [
            selection.filter_pitches("&", pitch.get_name(locale="us"))
            for pitch in pitch_tags
        ]
        for result in results:
            if not isinstance(result, abjad.Selection):
                raise TypeError
        return [result for result in results if isinstance(result, abjad.Selection)]


class DecodeCommand(Command):
    """
    Command to decode indicator.
    """

    def __call__(self, target):
        decode(target)


class QuantizeSequenceCommand(Command):
    r"""
    Quantize Sequence Command.

    ..  container:: example

        >>> template = pang.make_single_staff_score_template()
        >>> maker = pang.SegmentMaker(
        ...     score_template=template,
        ... )
        >>> instances = [0, 1, 2, 3]
        >>> durations = [1, 1, 0.5, 0.5]
        >>> sound_points_generator = pang.ManualSoundPointsGenerator(
        ...     instances=instances,
        ...     durations=durations,
        ... )
        >>> sequence = pang.Sequence(
        ...     sound_points_generator=sound_points_generator,
        ... )
        >>> command = pang.QuantizeSequenceCommand(sequence)
        >>> scope = pang.Scope(voice_name="Voice")
        >>> maker(scope, command)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file)
            >>> print(string)
            \version "2.20.0"
            \language "english"
            <BLANKLINE>
            #(ly:set-option 'relative-includes #t)
            <BLANKLINE>
            \include "source/_stylesheets/single-voice-staff.ily"
            <BLANKLINE>
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                <<
                    \context Voice = "Voice"
                    {
                        {
                            \tempo 4=60
                            \time 4/4
                            c'4
                            c'4
                            c'8
                            r8
                            c'8
                            r8
                        }
                    }
                >>
            >>
    """

    def __init__(
        self,
        sequence: Sequence,
        q_schema=None,
        grace_handler=None,
        heuristic=None,
        attack_point_optimizer: typing.Optional[nauert.AttackPointOptimizer] = None,
        attach_tempos: bool = True,
        tag_as_pitch: bool = False,
    ):
        self._sequence: Sequence = sequence
        self._q_schema = q_schema or nauert.MeasurewiseQSchema()
        self._grace_handler = grace_handler or nauert.ConcatenatingGraceHandler(
            replace_rest_with_final_grace_note=True
        )
        self._heuristic = heuristic or nauert.DistanceHeuristic()
        self._attack_point_optimizer = (
            attack_point_optimizer or nauert.MeasurewiseAttackPointOptimizer()
        )
        self._attach_tempos = attach_tempos
        self._quantizer = nauert.Quantizer()
        self._tag_as_pitch = tag_as_pitch

    def __call__(self, target: abjad.Voice):
        sequence = self._sequence
        sequence.simulate_queue(tag_as_pitch=self._tag_as_pitch)
        results = []
        for server in sequence.servers:
            q_event_sequence = server.q_event_sequence
            result = self._quantizer(
                q_event_sequence,
                q_schema=self._q_schema,
                grace_handler=self._grace_handler,
                heuristic=self._heuristic,
                attack_point_optimizer=self._attack_point_optimizer,
                attach_tempos=self._attach_tempos,
            )
            results.append(result)
        assert len(results) == 1
        result = results[0]
        target.extend(result)
