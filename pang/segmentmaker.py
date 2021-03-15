import abjad


class SegmentMaker:
    r"""
    Segment-maker.

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
            \include "lilypond/single-voice-staff.ily"
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
        environment=None,
        score_template=None,
    ):
        self._environment = environment
        self._score = score_template

    def __call__(self, scope, command):
        results = command()
        assert len(results) == 1
        result = results[0]
        self._score[scope.voice_name].extend(result)

    def _get_lilypond_includes(self):
        if self._environment == "docs":
            return ["source/_stylesheets/single-voice-staff.ily"]

    def _make_lilypond_file(self):
        includes = self._get_lilypond_includes()
        lilypond_file = abjad.LilyPondFile(
            items=[self._score], includes=includes, use_relative_includes=True
        )
        self._lilypond_file = lilypond_file

    @property
    def lilypond_file(self):
        return self._lilypond_file

    @property
    def score(self):
        return self._score

    def run(self, environment=None):
        self._environment = environment
        self._make_lilypond_file()
        return self.lilypond_file
