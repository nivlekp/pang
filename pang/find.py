from typing import Type

import abjad

from . import get


def q_event_attachment[T](leaf: abjad.Leaf, attachment_type: Type[T]) -> T | None:
    q_event_attachments = abjad.get.annotation(leaf, "q_event_attachments")
    if not q_event_attachments:
        return None
    attachments = [
        attachment
        for attachment in abjad.get.annotation(leaf, "q_event_attachments")
        if isinstance(attachment, attachment_type)
    ]
    if attachments:
        return attachments[0]
    return None


def next_q_event_attachment[T](
    logical_ties: list[abjad.LogicalTie], attachment_type: Type[T]
) -> T | None:
    for logical_tie in logical_ties:
        attachment = q_event_attachment(get.leaf(logical_tie, 0), attachment_type)
        if attachment is not None:
            return attachment
    return None
