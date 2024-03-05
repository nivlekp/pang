import abjad
import pang

VOICE_NAME = "Voice"


def test_build_section():
    score = make_score()
    scope = pang.Scope(voice_name=VOICE_NAME)
    command = make_command()
    metadata = pang.build.section(score, scope, command)

    assert metadata["last_metronome_mark"]["reference_duration"] == "1/4"
    assert metadata["last_metronome_mark"]["units_per_minute"] == 60
    assert metadata["last_time_signature"] == "4/4"
    assert metadata["empty_beatspan"] == "1/8"
    assert metadata["discarded_q_events_count"] == 0
    assert metadata["discarded_pitched_q_events_count"] == 0

    assert score[0]
    assert score[0][0]


def make_score():
    voice = abjad.Voice(name=VOICE_NAME)
    staff = abjad.Staff([voice], name="Staff")
    return abjad.Score([staff], name="Score")


def make_command():
    instances = [0, 1, 2, 3]
    durations = [1, 1, 0.5, 0.5]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
    )
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
    )
    return pang.QuantizeSequenceCommand(sequence)
