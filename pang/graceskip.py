import abjad


def _get_tuplet_multiplier(container):
    parentage = abjad.get.parentage(container)
    tuplets = [component for component in parentage if isinstance(component, abjad.Tuplet)]
    if tuplets == []:
        return abjad.NonreducedFraction((1, 1))
    multiplier = tuplets[0].multiplier
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
                stored_duration, stored_multiplier= longest_durations.get(
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
                    multiplier = multiplier.reduce()
                    if multiplier != 1:
                        for leaf in container:
                            leaf.multiplier = multiplier
            else:
                multiplier = stored_multiplier / multiplier
                multiplier = multiplier.reduce()
                if multiplier== 1:
                    skip = abjad.Skip(stored_duration)
                else:
                    skip = abjad.Skip(stored_duration, multiplier=multiplier)
                container = abjad.BeforeGraceContainer([skip])
                abjad.attach(container, first_leaf)
