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
        >>> string = abjad.lilypond(maker.score)
        >>> print(string)
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
        score_template=None,
    ):
        # self._lilypond_file = None
        self._score = score_template

    def __call__(self, scope, command):
        results = command()
        assert len(results) == 1
        result = results[0]
        self._score[scope.voice_name].extend(result)

    @property
    def score(self):
        return self._score
