import copy

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
        >>> sequence = pang.Sequence.from_sound_points_generator(
        ...     sound_points_generator, 4
        ... )
        >>> command = pang.QuantizeSequenceCommand(sequence)
        >>> scope = pang.Scope(voice_name="Voice")
        >>> maker(scope, command)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file)
            >>> print(string)
            \version "2.25.16"
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
        metadata = {}
        last_metronome_mark = self._get_last_metronome_mark()
        duration = last_metronome_mark.reference_duration
        reference_duration = f"{duration.numerator}/{duration.denominator}"
        units_per_minute = last_metronome_mark.units_per_minute
        metadata["last_metronome_mark"] = {
            "reference_duration": reference_duration,
            "units_per_minute": units_per_minute,
        }
        time_signature = self._get_last_time_signature()
        time_signature = f"{time_signature.numerator}/{time_signature.denominator}"
        metadata["last_time_signature"] = time_signature
        duration = self._get_empty_beatspan()
        metadata["empty_beatspan"] = f"{duration.numerator}/{duration.denominator}"
        metadata["segment_name"] = self._segment_name
        self._metadata.update(metadata)

    def _get_empty_beatspan(self):
        max_empty_beatspan = abjad.Duration(0)
        for staff in self._score:
            for voice in staff:
                empty_beatspan = abjad.Duration(0)
                for leaf in abjad.iterate.leaves(voice, reverse=True):
                    if isinstance(leaf, abjad.Rest):
                        empty_beatspan += leaf.written_duration
                    else:
                        break
                if empty_beatspan > max_empty_beatspan:
                    max_empty_beatspan = empty_beatspan
        return max_empty_beatspan

    def _get_first_tempo(self):
        first_leaf = abjad.get.leaf(self._score, 0)
        prototype = abjad.MetronomeMark
        return abjad.get.effective(first_leaf, prototype)

    def _get_first_time_signature(self):
        first_leaf = abjad.get.leaf(self._score, 0)
        prototype = abjad.TimeSignature
        return abjad.get.effective(first_leaf, prototype)

    def _get_last_metronome_mark(self):
        last_leaf = abjad.get.leaf(self._score, -1)
        prototype = abjad.MetronomeMark
        return abjad.get.effective(last_leaf, prototype)

    def _get_last_time_signature(self):
        last_leaf = abjad.get.leaf(self._score, -1)
        prototype = abjad.TimeSignature
        return abjad.get.effective(last_leaf, prototype)

    def _get_lilypond_includes(self):
        if self._environment == "docs":
            return ["source/_stylesheets/single-voice-staff.ily"]
        else:
            return ["../../stylesheets/stylesheet.ily"]

    def _make_build_file(self, previous_metadata=None):
        includes = self._get_lilypond_includes()
        build_file_score = copy.deepcopy(self._score)
        if previous_metadata is not None:
            first_tempo = self._get_first_tempo()
            first_time_signature = self._get_first_time_signature()
            first_leaf = abjad.get.leaf(build_file_score, 0)
            if first_tempo == previous_metadata["last_tempo"]:
                abjad.detach(abjad.MetronomeMark, first_leaf)
            if first_time_signature == previous_metadata["last_time_signature"]:
                abjad.detach(abjad.TimeSignature, first_leaf)
        items = [rf'\include "{include}"' for include in includes]
        items += self._score
        build_file = abjad.LilyPondFile(items=items)
        self._build_file = build_file

    def _make_lilypond_file(self):
        includes = self._get_lilypond_includes()
        items = ["#(ly:set-option 'relative-includes #t)"]
        items += [rf'\include "{include}"' for include in includes]
        items += [self._score]
        lilypond_file = abjad.LilyPondFile(items=items)
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
    def build_file(self):
        r"""
        Returns the build file for the score.
        """
        return self._build_file

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
            >>> sequence = pang.Sequence.from_sound_points_generator(
            ...     sound_points_generator, 4
            ... )
            >>> command = pang.QuantizeSequenceCommand(sequence)
            >>> scope = pang.Scope(voice_name="Voice")
            >>> maker(scope, command)
            >>> lilypond_file = maker.run(environment="docs")
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file)
                >>> print(string)
                \version "2.25.16"
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

            >>> import pprint
            >>> pprint.pprint(maker.metadata)
            {'empty_beatspan': '1/8',
             'last_metronome_mark': {'reference_duration': '1/4', 'units_per_minute': 60},
             'last_time_signature': '4/4',
             'segment_name': 'test'}
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
        # self._process_previous_metadata(previous_metadata)
        self._metadata = {} if metadata is None else dict(metadata)
        self._make_lilypond_file()
        self._make_build_file(previous_metadata=previous_metadata)
        self._collect_metadata()
        return self.lilypond_file
