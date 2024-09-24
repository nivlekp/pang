import abjad


def align_voices_length(voices: tuple[abjad.Voice, ...]) -> None:
    longest_voice = _find_longest_voice(voices)
    for voice in voices:
        _align_two_voices(voice, longest_voice)


def _find_longest_voice(voices: tuple[abjad.Voice, ...]) -> abjad.Voice:
    return abjad.Voice()


def _align_two_voices(shorter_voice: abjad.Voice, longer_voice: abjad.Voice) -> None:
    pass
