import abjad


def _get_longest_durations(voices):
    longest_durations = {}
    for voice in voices:
        for measure_number, measure in enumerate(voice):
            first_leaf = abjad.get.leaf(measure, 0)
            if abjad.get.grace(first_leaf):
                container = abjad.get.parentage(first_leaf).parent
                assert isinstance(container, abjad.BeforeGraceContainer)
                duration = abjad.get.duration(container)
                longest_duration = longest_durations.get(
                    measure_number, abjad.Duration(0)
                )
                if duration > longest_duration:
                    longest_durations[measure_number] = duration
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
            if abjad.get.grace(first_leaf):
                container = abjad.get.parentage(first_leaf).parent
                assert isinstance(container, abjad.BeforeGraceContainer)
                duration = abjad.get.duration(container)
                longest_duration = longest_durations[measure_number]
                if duration < longest_duration:
                    container.insert(0, abjad.Skip(longest_duration - duration))
            else:
                skip = abjad.Skip(longest_durations[measure_number])
                container = abjad.BeforeGraceContainer([skip])
                abjad.attach(container, first_leaf)
