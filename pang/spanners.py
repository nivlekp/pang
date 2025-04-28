import abjad


def glissando_to_next_leaf(logical_tie: abjad.LogicalTie) -> None:
    all_leaves = abjad.select.with_next_leaf(logical_tie)
    logical_tie_leaves = all_leaves[:-1]
    _untie_logical_tie(logical_tie_leaves)
    timespan = float(abjad.get.timespan(logical_tie_leaves).duration)
    current_time = float(abjad.get.duration(logical_tie_leaves[0]))
    starting_pitch = next(iter(abjad.get.pitches(all_leaves[0])))
    destination_pitch = next(iter(abjad.get.pitches(all_leaves[-1])))
    for leaf in logical_tie_leaves[1:]:
        pitch_number = round((destination_pitch.number - starting_pitch.number) * current_time / timespan)
        assert isinstance(leaf, abjad.Note)
        leaf.written_pitch = pitch_number
        current_time += float(abjad.get.duration(leaf))
    abjad.glissando(all_leaves, allow_repeats=True, hide_middle_note_heads=True)


def _untie_logical_tie(leaves: list[abjad.Leaf]) -> None:
    for leaf in leaves[:-1]:
        abjad.detach(abjad.indicators.Tie, leaf)
