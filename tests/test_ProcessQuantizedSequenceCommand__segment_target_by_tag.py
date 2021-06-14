import abjad
import pang


def test_ProcessQuantizedSequenceCommand__segment_target_by_tag_00():
    instances = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    sound_points_generator = pang.ManualSoundPointsGenerator(
        instances=instances,
        durations=durations,
    )
    sequence_duration = 10
    sequence = pang.Sequence(
        sound_points_generator=sound_points_generator,
        sequence_duration=sequence_duration,
    )
    for event in sequence[:5]:
        event.tag = 0
    for event in sequence[5:]:
        event.tag = 1
    # The sequence is just a dummy to init the command and to provide the tags
    command = pang.ProcessQuantizedSequenceCommand(sequence)
    voice = abjad.Voice("c'4 c'4~ c'8 cs'8 cs'4")
    segments = command._segment_target_by_tag(target=voice)
    assert segments[0] == abjad.select(voice[:3]).logical_ties()
    assert segments[1] == abjad.select(voice[3:]).logical_ties()
