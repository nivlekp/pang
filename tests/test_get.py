import pytest

import abjad
import pang


def test_get_leaf__leaf_exists() -> None:
    voice = abjad.Voice("c'4 d'4 e'4 f'4")
    assert abjad.lilypond(pang.get.leaf(voice, 0)) == "c'4"


def test_get_leaf__leaf_absent() -> None:
    voice = abjad.Voice()
    with pytest.raises(ValueError):
        pang.get.leaf(voice, 0)
