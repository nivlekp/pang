import abjad
import pang


def test_find_q_event_attachment() -> None:
    voice = abjad.Voice("c'4")
    leaf = abjad.get.leaf(voice, 0)
    abjad.annotate(leaf, "q_event_attachments", [abjad.Dynamic("p"), abjad.ColorFingering(1)])
    assert pang.find.q_event_attachment(leaf, abjad.Dynamic) == abjad.Dynamic("p")
    assert pang.find.q_event_attachment(leaf, abjad.ColorFingering) == abjad.ColorFingering(1)
