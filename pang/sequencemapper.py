import dataclasses

from .sequences import Sequence


@dataclasses.dataclass(frozen=True)
class QuantizingMetadata:
    pass


@dataclasses.dataclass(frozen=True)
class VoiceSpecification:
    pass


def populate_voices_from_sequence(
    sequence: Sequence, voice_specifications: tuple[VoiceSpecification, ...]
) -> QuantizingMetadata:
    raise NotImplementedError
