import abjad
import pang

from .utils import to_sound_points


def test_populate_voices_from_sequence_noop() -> None:
    voice = abjad.Voice()
    metadata = pang.populate_voices_from_sequence(
        pang.Sequence.empty_sequence(),
        (pang.VoiceSpecification(voice),),
    )
    assert len(voice) == 0
    assert metadata.number_of_all_discarded_q_events == 0
    assert metadata.number_of_discarded_pitched_q_events == 0


def test_populate_voices_from_sequence() -> None:
    voice = abjad.Voice()
    metadata = pang.populate_voices_from_sequence(
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
    assert metadata.number_of_all_discarded_q_events == 0
    assert metadata.number_of_discarded_pitched_q_events == 0
