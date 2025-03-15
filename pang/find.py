from typing import Type, TypeVar

import abjad

T = TypeVar("T")


def q_event_attachment(leaf: abjad.Leaf, attachment_type: Type[T]) -> T | None:
    attachments = [
        attachment
        for attachment in abjad.get.annotation(leaf, "q_event_attachments")
        if isinstance(attachment, attachment_type)
    ]
    if attachments:
        return attachments[0]
    return None
