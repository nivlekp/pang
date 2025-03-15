import abjad


def glissando_to_next_leaf(logical_tie: abjad.LogicalTie) -> None:
    all_leaves = abjad.select.with_next_leaf(logical_tie)
    logical_tie_leaves = all_leaves[:-1]
    next_leaf = all_leaves[-1]
    _untie_logical_tie(logical_tie_leaves)
    abjad.glissando(all_leaves, allow_repeats=True, hide_middle_note_heads=True)


def _untie_logical_tie(leaves: list[abjad.Leaf]) -> None:
    for leaf in leaves[:-1]:
        abjad.detach(abjad.indicators.Tie, leaf)
