import abjad
import pang


def test_find_q_event_attachment__attachment_present() -> None:
    voice = abjad.Voice("c'4")
    leaf = abjad.get.leaf(voice, 0)
    assert leaf is not None
    abjad.annotate(
        leaf, "q_event_attachments", [abjad.Dynamic("p"), abjad.ColorFingering(1)]
    )
    assert pang.find.q_event_attachment(leaf, abjad.Dynamic) == abjad.Dynamic("p")
    assert pang.find.q_event_attachment(
        leaf, abjad.ColorFingering
    ) == abjad.ColorFingering(1)


def test_find_q_event_attachment__attachment_absent() -> None:
    voice = abjad.Voice("c'4")
    leaf = abjad.get.leaf(voice, 0)
    assert leaf is not None
    abjad.annotate(leaf, "q_event_attachments", [abjad.ColorFingering(1)])
    assert pang.find.q_event_attachment(leaf, abjad.Dynamic) is None
