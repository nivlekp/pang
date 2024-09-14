import dataclasses

import abjad
from abjadext import nauert

from .noteserver import NoteServer
from .sequences import Sequence


@dataclasses.dataclass(frozen=True)
class QuantizingMetadata:
    pass


@dataclasses.dataclass(frozen=True)
class VoiceSpecification:
    voice: abjad.Voice
    note_server: NoteServer = dataclasses.field(default_factory=NoteServer)
    q_schema: nauert.QSchema = dataclasses.field(default_factory=nauert.BeatwiseQSchema)
    grace_handler: nauert.GraceHandler = dataclasses.field(
        default_factory=nauert.ConcatenatingGraceHandler
    )
    heuristic: nauert.Heuristic = dataclasses.field(
        default_factory=nauert.DistanceHeuristic
    )
    attack_point_optimizer: nauert.AttackPointOptimizer = dataclasses.field(
        default_factory=nauert.MeasurewiseAttackPointOptimizer
    )
    attach_tempos: bool = True


def populate_voices_from_sequence(
    sequence: Sequence, voice_specifications: tuple[VoiceSpecification, ...]
) -> QuantizingMetadata:
    return QuantizingMetadata()
