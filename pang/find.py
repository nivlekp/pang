from typing import Type, TypeVar

import abjad

T = TypeVar("T")


class AttachmentNotFoundError(ValueError):
    pass


def q_event_attachment(leaf: abjad.Leaf, attachment_type: Type[T]) -> T:
    attachments = [
        attachment
        for attachment in abjad.get.annotation(leaf, "q_event_attachments")
        if isinstance(attachment, attachment_type)
    ]
    if attachments:
        return attachments[0]
    raise AttachmentNotFoundError
