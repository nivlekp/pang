import fractions

import abjad


def _get_tuplet_multiplier(container):
    parentage = abjad.get.parentage(container)
    tuplets = [
        component for component in parentage if isinstance(component, abjad.Tuplet)
    ]
    if tuplets == []:
        return fractions.Fraction(1, 1)
    multiplier = fractions.Fraction(*tuplets[0].multiplier)
    for tuplet in tuplets[1:]:
        multiplier = multiplier.multiply_with_cross_cancelation(tuplet.multiplier)
    return multiplier


def _get_longest_durations(voices):
    longest_durations = {}
    for voice in voices:
        for measure_number, measure in enumerate(voice):
            first_leaf = abjad.get.leaf(measure, 0)
            if abjad.get.grace(first_leaf):
                container = abjad.get.parentage(first_leaf).parent
                assert isinstance(container, abjad.BeforeGraceContainer)
                duration = abjad.get.duration(container)
                multiplier = _get_tuplet_multiplier(container)
                stored_duration, stored_multiplier = longest_durations.get(
                    measure_number, (abjad.Duration(0), 1)
                )
                if duration > stored_duration:
                    longest_durations[measure_number] = (duration, multiplier)
                elif duration == stored_duration and multiplier > stored_multiplier:
                    longest_durations[measure_number] = (duration, multiplier)
    return longest_durations


def pad_voices_with_grace_skips(voices):
    """
    Pad voices with grace skips to fix the spacing issue with full-length
    tuplet brackets.
    """
    longest_durations = _get_longest_durations(voices)
    for voice in voices:
        for measure_number in longest_durations:
            first_leaf = abjad.get.leaf(voice[measure_number], 0)
            multiplier = _get_tuplet_multiplier(first_leaf)
            stored_duration, stored_multiplier = longest_durations[measure_number]
            if abjad.get.grace(first_leaf):
                container = abjad.get.parentage(first_leaf).parent
                assert isinstance(container, abjad.BeforeGraceContainer)
                duration = abjad.get.duration(container)
                if duration < stored_duration:
                    container.insert(0, abjad.Skip(stored_duration - duration))
                if multiplier != stored_multiplier:
                    multiplier = stored_multiplier / multiplier
                    if multiplier != 1:
                        for leaf in container:
                            leaf.multiplier = multiplier.as_integer_ratio()
            else:
                multiplier = stored_multiplier / multiplier
                if multiplier == 1:
                    skip = abjad.Skip(stored_duration)
                else:
                    skip = abjad.Skip(
                        stored_duration, multiplier=multiplier.as_integer_ratio()
                    )
                container = abjad.BeforeGraceContainer([skip])
                abjad.attach(container, first_leaf)


class OttavaHandler:
    """
    Ottava Handler.
    """

    def __call__(self, voice):
        raise NotImplementedError


class ManualOttavaHandler(OttavaHandler):
    """
    Manual Ottava Handler.
    """

    def __init__(self, n=1):
        self._n = n

    def __call__(self, voice):
        first_leaf = abjad.get.leaf(voice, 0)
        ottava = abjad.Ottava(n=self.n)
        abjad.attach(ottava, first_leaf)

    @property
    def n(self):
        return self._n


class VerboseOttavaHandler(OttavaHandler):
    """
    Verbose Ottava Handler.
    """

    def __init__(self, high_threshold=32, low_threshold=-31):
        self._high_threshold = high_threshold
        self._low_threshold = low_threshold

    def __call__(self, voice):
        for logical_tie in abjad.iterate.logical_ties(voice):
            leaf = logical_tie[0]
            if isinstance(leaf, abjad.Rest):
                continue
            assert isinstance(leaf, abjad.Note)
            if leaf.written_pitch > self.high_threshold:
                self._attach_note_name(leaf, abjad.UP)
            if leaf.written_pitch < self.low_threshold:
                self._attach_note_name(leaf, abjad.DOWN)

    def _attach_note_name(self, leaf, direction):
        assert isinstance(leaf, abjad.Note)
        pitch_name = leaf.written_pitch.pitch_class.name[0]
        string = rf"\markup {{ {pitch_name} }}"
        markup = abjad.Markup(string)
        abjad.attach(markup, leaf, direction=direction)

    @property
    def high_threshold(self):
        return self._high_threshold

    @property
    def low_threshold(self):
        return self._low_threshold
