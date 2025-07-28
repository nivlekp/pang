import abjad


def glissando_to_next_leaf(logical_tie: abjad.LogicalTie) -> None:
    all_leaves = abjad.select.with_next_leaf(logical_tie)
    logical_tie_leaves = all_leaves[:-1]
    _untie_logical_tie(logical_tie_leaves)
    _adjust_pitch(logical_tie_leaves, all_leaves[-1])
    abjad.glissando(all_leaves, allow_repeats=True, hide_middle_note_heads=True)


def _untie_logical_tie(leaves: list[abjad.Leaf]) -> None:
    for leaf in leaves[:-1]:
        abjad.detach(abjad.indicators.Tie, leaf)


def _adjust_pitch(logical_tie_leaves: list[abjad.Leaf], next_leaf: abjad.Leaf) -> None:
    timespan = float(abjad.get.timespan(logical_tie_leaves).get_duration())
    current_time = float(abjad.get.duration(logical_tie_leaves[0]))
    starting_pitch = next(iter(abjad.get.pitches(logical_tie_leaves[0])))
    destination_pitch = next(iter(abjad.get.pitches(next_leaf)))
    for leaf in logical_tie_leaves[1:]:
        pitch_number = round(
            (destination_pitch.get_number() - starting_pitch.get_number())
            * current_time
            / timespan
            + starting_pitch.get_number()
        )
        assert isinstance(leaf, abjad.Note)
        leaf.written_pitch = abjad.NamedPitch(pitch_number)
        current_time += float(abjad.get.duration(leaf))
