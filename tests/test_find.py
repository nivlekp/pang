import abjad
import pang


def test_find_q_event_attachment__attachment_present() -> None:
    voice = abjad.Voice("c'4")
    leaf = pang.get.leaf(voice, 0)
    abjad.annotate(
        leaf, "q_event_attachments", [abjad.Dynamic("p"), abjad.ColorFingering(1)]
    )
    assert pang.find.q_event_attachment(leaf, abjad.Dynamic) == abjad.Dynamic("p")
    assert pang.find.q_event_attachment(
        leaf, abjad.ColorFingering
    ) == abjad.ColorFingering(1)


def test_find_q_event_attachment__attachment_absent() -> None:
    voice = abjad.Voice("c'4")
    leaf = pang.get.leaf(voice, 0)
    abjad.annotate(leaf, "q_event_attachments", [abjad.ColorFingering(1)])
    assert pang.find.q_event_attachment(leaf, abjad.Dynamic) is None


def test_find_q_event_attachment__q_events_attachments_absent() -> None:
    assert (
        pang.find.q_event_attachment(
            pang.get.leaf(abjad.Voice("c'4"), 0), abjad.Dynamic
        )
        is None
    )


def test_find_next_q_event_attachment__present() -> None:
    voice = abjad.Voice("c'4 c'4 c'4 c'4")
    abjad.annotate(voice[2], "q_event_attachments", [abjad.Dynamic("p")])
    assert pang.find.q_event_attachment(voice[2], abjad.Dynamic) == abjad.Dynamic("p")


def test_find_next_q_event_attachment__absent() -> None:
    voice = abjad.Voice("c'4 c'4 c'4 c'4")
    assert pang.find.q_event_attachment(voice[2], abjad.Dynamic) is None
