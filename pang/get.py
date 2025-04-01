import abjad


def leaf(argument: abjad.Voice | abjad.LogicalTie, index: int) -> abjad.Leaf:
    leaf = abjad.get.leaf(argument, index)
    if leaf is None:
        raise ValueError(f"Leaf not found in {argument}")
    return leaf
