import nauert

import abjad
import pang

from .utils import to_sound_points


def test_populate_voices_from_sequence_noop() -> None:
    voice = abjad.Voice(name="voice_name")
    metadata = pang.populate_voices_from_sequence(
        pang.Sequence.empty_sequence(),
        (pang.VoiceSpecification(voice),),
    )
    assert len(voice) == 0
    assert metadata["voice_name"].number_of_all_discarded_q_events == 0
    assert metadata["voice_name"].number_of_discarded_pitched_q_events == 0


def test_populate_voices_from_sequence_without_discarded_q_events() -> None:
    voice = abjad.Voice(name="voice_name")
    metadata = pang.populate_voices_from_sequence(
        pang.Sequence(to_sound_points([0, 1], [1, 1], [0, 0]), 2),
        (pang.VoiceSpecification(voice),),
    )
    string = abjad.lilypond(voice)
    assert string == abjad.string.normalize(
        r"""
        \context Voice = "voice_name"
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
    assert metadata["voice_name"].number_of_all_discarded_q_events == 0
    assert metadata["voice_name"].number_of_discarded_pitched_q_events == 0


def test_populate_voices_from_sequence_with_a_discarded_silent_q_event() -> None:
    voice = abjad.Voice(name="voice_name")
    metadata = pang.populate_voices_from_sequence(
        pang.Sequence(to_sound_points([0, 1.01], [1, 1], [0, 0]), 2),
        (
            pang.VoiceSpecification(
                voice, grace_handler=nauert.DiscardingGraceHandler()
            ),
        ),
    )
    string = abjad.lilypond(voice)
    assert string == abjad.string.normalize(
        r"""
        \context Voice = "voice_name"
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
    assert metadata["voice_name"].number_of_all_discarded_q_events == 1
    assert metadata["voice_name"].number_of_discarded_pitched_q_events == 0


def test_populate_voices_from_sequence_with_a_discarded_pitched_q_event() -> None:
    voice = abjad.Voice(name="voice_name")
    metadata = pang.populate_voices_from_sequence(
        pang.Sequence(to_sound_points([0, 1, 1.01], [1, 0.01, 1], [0, 0, 0]), 2),
        (
            pang.VoiceSpecification(
                voice, grace_handler=nauert.DiscardingGraceHandler()
            ),
        ),
    )
    string = abjad.lilypond(voice)
    assert string == abjad.string.normalize(
        r"""
        \context Voice = "voice_name"
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
    assert metadata["voice_name"].number_of_all_discarded_q_events == 1
    assert metadata["voice_name"].number_of_discarded_pitched_q_events == 1
