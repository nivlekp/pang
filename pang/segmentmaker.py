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
        segment_name=None,
    ):
        self._environment = environment
        self._score = score_template
        self._segment_name = segment_name

    def __call__(self, scope, command):
        target = self._score[scope.voice_name]
        command(target)

    def _collect_metadata(self):
        metadata = abjad.OrderedDict()
        metadata["last_tempo"] = self._get_last_tempo()
        metadata["last_time_signature"] = self._get_last_time_signature()
        metadata["empty_beatspan"] = self._get_empty_beatspan()
        metadata["segment_name"] = self._segment_name
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

    def _get_first_tempo(self):
        voice = self._score[0][0]
        first_leaf = abjad.get.leaf(voice, 0)
        prototype = abjad.MetronomeMark
        return abjad.get.effective(first_leaf, prototype)

    def _get_first_time_signature(self):
        voice = self._score[0][0]
        first_leaf = abjad.get.leaf(voice, 0)
        prototype = abjad.TimeSignature
        return abjad.get.effective(first_leaf, prototype)

    def _get_last_tempo(self):
        voice = self._score[0][0]
        last_leaf = abjad.get.leaf(voice, -1)
        prototype = abjad.MetronomeMark
        return abjad.get.effective(last_leaf, prototype)

    def _get_last_time_signature(self):
        voice = self._score[0][0]
        last_leaf = abjad.get.leaf(voice, -1)
        prototype = abjad.TimeSignature
        return abjad.get.effective(last_leaf, prototype)

    def _get_lilypond_includes(self):
        if self._environment == "docs":
            return ["source/_stylesheets/single-voice-staff.ily"]
        else:
            return ["../../stylesheets/stylesheet.ily"]

    def _make_lilypond_file(self):
        includes = self._get_lilypond_includes()
        lilypond_file = abjad.LilyPondFile(
            items=[self._score], includes=includes, use_relative_includes=True
        )
        self._lilypond_file = lilypond_file

    def _process_previous_metadata(self, previous_metadata):
        if previous_metadata is None:
            return
        first_tempo = self._get_first_tempo()
        first_time_signature = self._get_first_time_signature()
        voice = self._score[0][0]
        first_leaf = abjad.get.leaf(voice, 0)
        if first_tempo == previous_metadata["last_tempo"]:
            abjad.detach(abjad.MetronomeMark, first_leaf)
        if first_time_signature == previous_metadata["last_time_signature"]:
            abjad.detach(abjad.TimeSignature, first_leaf)

    @property
    def metadata(self):
        r"""
        Returns metadata.

        ..  container:: example

            >>> template = pang.make_single_staff_score_template()
            >>> maker = pang.SegmentMaker(
            ...     score_template=template,
            ...     segment_name="test",
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
                        'last_tempo',
                        abjad.MetronomeMark(
                            reference_duration=abjad.Duration(1, 4),
                            units_per_minute=60,
                            ),
                        ),
                    (
                        'last_time_signature',
                        abjad.TimeSignature((4, 4)),
                        ),
                    (
                        'empty_beatspan',
                        abjad.Duration(1, 8),
                        ),
                    ('segment_name', 'test'),
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

    @property
    def segment_name(self):
        """
        Returns segment's name.
        """
        return self._segment_name

    def run(self, environment=None, metadata=None, previous_metadata=None):
        """
        Runs the segment-maker.
        """
        self._environment = environment
        self._process_previous_metadata(previous_metadata)
        self._metadata = abjad.OrderedDict(metadata)
        self._make_lilypond_file()
        self._collect_metadata()
        return self.lilypond_file
