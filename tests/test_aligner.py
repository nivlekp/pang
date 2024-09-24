import abjad
from pang import aligner


def test_align_voices_length_noop():
    voices = (abjad.Voice("c'4"), abjad.Voice("c'4"))
    aligner.align_voices_length(voices)
    assert all(len(voice) == 1 for voice in voices)


def test_align_voices_length_simple():
    voices = (abjad.Voice("c'4 c'4"), abjad.Voice("c'4"))
    aligner.align_voices_length(voices)
    assert len(voices[0]) == 2
    assert len(voices[1]) == 2
