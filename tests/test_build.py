import abjad
import pang

VOICE_NAME = "Voice"


def test_collect_metadata() -> None:
    score = make_score()
    metadata = pang.build.collect_metadata(
        score, {VOICE_NAME: pang.sequencemapper.QuantizingMetadata(0, 0)}
    )

    last_metronome_mark = metadata["last_metronome_mark"]
    assert last_metronome_mark["reference_duration"] == "1/4"
    assert last_metronome_mark["units_per_minute"] == 60
    assert metadata["last_time_signature"] == "4/4"
    assert metadata["empty_beatspan"] == "1/8"
    voice_metadata = metadata["per_voice_metadata"][VOICE_NAME]
    assert voice_metadata["number_of_all_discarded_q_events"] == 0
    assert voice_metadata["number_of_discarded_pitched_q_events"] == 0


def make_score() -> abjad.Score:
    voice = abjad.Voice("c'4 c'4 c'4 c'8 r8", name=VOICE_NAME)
    first_leaf = pang.get.leaf(voice, 0)
    abjad.attach(abjad.MetronomeMark(abjad.Duration(1, 4), 60), first_leaf)
    abjad.attach(abjad.TimeSignature((4, 4)), first_leaf)
    staff = abjad.Staff([voice], name="Staff")
    return abjad.Score([staff], name="Score")
