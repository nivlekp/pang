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


def test_align_voices_length_consistent_time_signature() -> None:
    voice_0 = abjad.Voice("c'4 c'4 c'4 c'4 c'4 c'4")
    voice_1 = abjad.Voice("c'4 c'4")
    # put this in a staff group within a score to make time signatures visible
    abjad.Score([abjad.StaffGroup([voice_0, voice_1])])
    abjad.attach(abjad.TimeSignature((2, 4)), abjad.get.leaf(voice_0, 0))
    abjad.attach(abjad.TimeSignature((2, 4)), abjad.get.leaf(voice_1, 0))
    voices = (voice_0, voice_1)
    aligner.align_voices_length(voices)
    assert abjad.lilypond(voices[0]) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \time 2/4
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
            \time 2/4
            c'4
            c'4
            R2
            R2
        }
        """
    )


def test_align_voices_length_varying_time_signature() -> None:
    voices = (
        abjad.Voice(r"\time 3/8 c'8 c'8 c'8 \time 2/4 c'4 c'4 \time 3/8 c'8 c'8 c'8"),
        abjad.Voice(r"\time 3/8 c'8 c'8 r8"),
    )
    # put this in a staff group within a score to make time signatures visible
    abjad.Score([abjad.StaffGroup(list(voices))])
    aligner.align_voices_length(voices)
    assert abjad.lilypond(voices[0]) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \time 3/8
            c'8
            c'8
            c'8
            \time 2/4
            c'4
            c'4
            \time 3/8
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
            \time 3/8
            c'8
            c'8
            r8
            \time 2/4
            R2
            \time 3/8
            R4.
        }
        """
    )
