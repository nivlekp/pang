import abjad

from . import get


def align_voices_length(voices: tuple[abjad.Voice, ...]) -> None:
    longest_voice = max(voices, key=_number_of_measures)
    if len(longest_voice) == 0:
        return
    for voice in voices:
        _align_two_voices(voice, longest_voice)


def _number_of_measures(voice: abjad.Voice) -> int:
    if len(voice) == 0:
        return 0
    return abjad.get.measure_number(abjad.get.leaf(voice, -1))


def _align_two_voices(shorter_voice: abjad.Voice, longer_voice: abjad.Voice) -> None:
    last_time_signature = abjad.get.effective_indicator(
        get.leaf(shorter_voice, -1), abjad.TimeSignature
    )
    for measure in abjad.select.group_by_measure(longer_voice)[
        _number_of_measures(shorter_voice) :
    ]:
        rest = abjad.MultimeasureRest(abjad.get.duration(measure))
        time_signature = abjad.get.effective_indicator(measure[0], abjad.TimeSignature)
        if time_signature is not None and time_signature != last_time_signature:
            abjad.attach(time_signature, rest)
            last_time_signature = time_signature
        shorter_voice.extend([rest])
