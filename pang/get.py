import abjad


def leaf(voice: abjad.Voice, index: int) -> abjad.Leaf:
    leaf = abjad.get.leaf(voice, index)
    if leaf is None:
        raise ValueError(f"Leaf not found in {voice}")
    return leaf
