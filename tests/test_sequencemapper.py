import pytest

import abjad
import pang

from .utils import to_sound_points


def test_populate_voices_from_sequence() -> None:
    voice = abjad.Voice()
    pang.populate_voices_from_sequence(
        pang.Sequence(to_sound_points([0, 1], [1, 1], [0, 0]), 2),
        (pang.VoiceSpecification(voice),),
    )
    string = abjad.lilypond(voice)
    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                %%% \time 4/4 %%%
                \tempo 4=60
                c'4
                c'4
                r2
            }
        }
        """
    ), print(string)
