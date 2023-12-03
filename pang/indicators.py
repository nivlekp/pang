import abjad


class Indicator:
    """
    Indicator base class. This is to support attaching indicators before
    quantizing using Nauert.
    """

    def __call__(self, target: abjad.LogicalTie):
        raise NotImplementedError


class Dynamic(Indicator):
    r"""
    This class attaches dynamic to a SoundPoint.

    ..  container:: example

        >>> template = pang.make_single_staff_score_template()
        >>> maker = pang.SegmentMaker(
        ...     score_template=template,
        ... )
        >>> instances = [0, 1, 1.5, 3]
        >>> durations = [1, 0.5, 1.5, 1]
        >>> pitches = [0, 0, (0, 12), 0]
        >>> sound_points_generator = pang.ManualSoundPointsGenerator(
        ...     instances=instances,
        ...     durations=durations,
        ...     pitches=pitches,
        ... )
        >>> sequence = pang.Sequence(
        ...     sound_points_generator=sound_points_generator,
        ... )
        >>> dynamic_names = ["p", "mp", "mf", "f"]
        >>> for event, dynamic_name in zip(sequence, dynamic_names):
        ...     dynamic = pang.Dynamic(dynamic_name)
        ...     event.attach(dynamic)
        ...
        >>> command = pang.QuantizeSequenceCommand(sequence)
        >>> scope = pang.Scope(voice_name="Voice")
        >>> maker(scope, command)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file)
            >>> print(string)
            \version "2.24.3"
            \language "english"
            #(ly:set-option 'relative-includes #t)
            \include "source/_stylesheets/single-voice-staff.ily"
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
                            \p
                            c'8
                            \mp
                            <c' c''>8
                            \mf
                            ~
                            <c' c''>4
                            c'4
                            \f
                        }
                    }
                >>
            >>
    """

    def __init__(self, value):
        assert isinstance(value, str)
        assert abjad.Dynamic.is_dynamic_name(value)
        self._dynamic = abjad.Dynamic(value)

    def __call__(self, target: abjad.LogicalTie):
        """
        Call indicator to process the target after quantizing.
        """
        for logical_tie in abjad.iterate.logical_ties(target, pitched=True):
            leaf = abjad.get.leaf(logical_tie)
            abjad.attach(self._dynamic, leaf)


class Red(Indicator):
    r"""
    Encoding and attaching the color red.

    ..  container:: example

        >>> template = pang.make_single_staff_score_template()
        >>> maker = pang.SegmentMaker(
        ...     score_template=template,
        ... )
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
        ...     event.attach(pang.Red())
        ...
        >>> command = pang.QuantizeSequenceCommand(sequence)
        >>> scope = pang.Scope(voice_name="Voice")
        >>> maker(scope, command)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file)
            >>> print(string)
            \version "2.24.3"
            \language "english"
            #(ly:set-option 'relative-includes #t)
            \include "source/_stylesheets/single-voice-staff.ily"
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                <<
                    \context Voice = "Voice"
                    {
                        {
                            \tempo 4=60
                            \time 4/4
                            \tweak color #red
                            c'4
                            \tweak color #red
                            c'4
                            <
                                \tweak color #red
                                c'
                                \tweak color #red
                                c''
                            >8
                            r8
                            \tweak color #red
                            c'8
                            r8
                        }
                    }
                >>
            >>
    """

    def __call__(self, target: abjad.LogicalTie):
        """
        Call indicator to process the target after quantizing.
        """
        for leaf in abjad.iterate.leaves(target, pitched=True):
            if isinstance(leaf, abjad.Chord):
                for note_head in leaf.note_heads:
                    abjad.tweak(note_head, r"\tweak color #red")
            if isinstance(leaf, abjad.Note):
                abjad.tweak(leaf.note_head, r"\tweak color #red")


class Harmonics(Indicator):
    r"""
    Encoding and attaching harmonics.

    ..  container:: example

        >>> template = pang.make_single_staff_score_template()
        >>> maker = pang.SegmentMaker(
        ...     score_template=template,
        ... )
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
        ...     event.attach(harmonics)
        ...
        >>> command = pang.QuantizeSequenceCommand(sequence)
        >>> scope = pang.Scope(voice_name="Voice")
        >>> maker(scope, command)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file)
            >>> print(string)
            \version "2.24.3"
            \language "english"
            #(ly:set-option 'relative-includes #t)
            \include "source/_stylesheets/single-voice-staff.ily"
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                <<
                    \context Voice = "Voice"
                    {
                        {
                            \tempo 4=60
                            \time 4/4
                            \tweak NoteHead.style #'harmonic
                            c'4
                            \tweak NoteHead.style #'harmonic
                            c'4
                            <
                                \tweak NoteHead.style #'harmonic
                                c'
                                c''
                            >8
                            r8
                            \tweak NoteHead.style #'harmonic
                            c'8
                            r8
                        }
                    }
                >>
            >>
    """

    def __init__(self):
        # TODO: initialize with harmonics if required
        pass

    def __call__(self, target: abjad.LogicalTie):
        """
        Call indicator to process the target after quantizing.
        """
        for leaf in abjad.iterate.leaves(target, pitched=True):
            if isinstance(leaf, abjad.Chord):
                note_head = leaf.note_heads[0]
            else:
                assert isinstance(leaf, abjad.Note)
                note_head = leaf.note_head
            abjad.tweak(note_head, r"\tweak NoteHead.style #'harmonic")
