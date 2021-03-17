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

    def _collect_metadata(self):
        metadata = abjad.OrderedDict()
        metadata["last_time_signature"] = self._get_last_time_signature()
        metadata["empty_beatspan"] = self._get_empty_beatspan()
        self.metadata.update(metadata)

    def _get_empty_beatspan(self):
        max_empty_beatspan = abjad.Duration(0)
        for staff in self._score:
            for voice in staff:
                empty_beatspan = abjad.Duration(0)
                for leaf in abjad.iterate(voice).leaves(reverse=True):
                    if isinstance(leaf, abjad.Rest):
                        empty_beatspan += leaf.written_duration
                    else:
                        break
                if empty_beatspan > max_empty_beatspan:
                    max_empty_beatspan = empty_beatspan
        return max_empty_beatspan

    def _get_last_time_signature(self):
        voice = self._score[0][0]
        last_leaf = abjad.get.leaf(voice, -1)
        prototype = abjad.TimeSignature
        return abjad.get.effective(last_leaf, prototype)

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
    def metadata(self):
        r"""
        Returns metadata.

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

        ..  container:: example

            >>> string = abjad.storage(maker.metadata)
            >>> print(string)
            abjad.OrderedDict(
                [
                    (
                        'last_time_signature',
                        abjad.TimeSignature((4, 4)),
                        ),
                    (
                        'empty_beatspan',
                        abjad.Duration(1, 8),
                        ),
                    ]
                )
        """
        return self._metadata

    @property
    def lilypond_file(self):
        """
        Returns LilyPond file.
        """
        return self._lilypond_file

    @property
    def score(self):
        """
        Returns Score.
        """
        return self._score

    def run(self, environment=None, metadata=None):
        """
        Runs the segment-maker.
        """
        self._environment = environment
        self._metadata = abjad.OrderedDict(metadata)
        self._make_lilypond_file()
        self._collect_metadata()
        return self.lilypond_file
