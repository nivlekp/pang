import abjad
from pang import aligner


def test_align_voices_length_noop() -> None:
    voices = (abjad.Voice(" ".join(["c'4"] * 4)), abjad.Voice(" ".join(["c'4"] * 4)))
    aligner.align_voices_length(voices)
    assert all(len(voice) == 4 for voice in voices)


def test_align_voices_length_simple() -> None:
    voices = (abjad.Voice(" ".join(["c'4"] * 8)), abjad.Voice(" ".join(["c'4"] * 4)))
    aligner.align_voices_length(voices)
    assert abjad.lilypond(voices[0]) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            c'4
            c'4
            c'4
            c'4
            c'4
            c'4
            c'4
        }
        """
    )
    assert abjad.lilypond(voices[1]) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            c'4
            c'4
            c'4
            R1
        }
        """
    )


def test_align_voices_length_varying_time_signature() -> None:
    voices = (
        abjad.Voice(r"\time 3/8 c'8 c'8 c'8 \time 2/4 c'4 c'4 \time 3/8 c'8 c'8 c'8"),
        abjad.Voice(r"\time 3/8 c'8 c'8 r8"),
    )
    aligner.align_voices_length(voices)
    assert abjad.lilypond(voices[0]) == abjad.string.normalize(
        r"""
        \new Voice
        {
            %%% \time 3/8 %%%
            c'8
            c'8
            c'8
            %%% \time 2/4 %%%
            c'4
            c'4
            %%% \time 3/8 %%%
            c'8
            c'8
            c'8
        }
        """
    )
    assert abjad.lilypond(voices[1]) == abjad.string.normalize(
        r"""
        \new Voice
        {
            %%% \time 3/8 %%%
            c'8
            c'8
            r8
            %%% \time 2/4 %%%
            R2
            %%% \time 3/8 %%%
            R4.
        }
        """
    )
