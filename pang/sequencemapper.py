import dataclasses

import abjad
from abjadext import nauert

from .noteserver import NoteServer
from .queuesimulation import simulate_queue
from .sequences import Sequence


@dataclasses.dataclass(frozen=True)
class QuantizingMetadata:
    pass


@dataclasses.dataclass(frozen=True)
class VoiceSpecification:
    voice: abjad.Voice
    note_server: NoteServer = dataclasses.field(default_factory=NoteServer)
    q_schema: nauert.QSchema = dataclasses.field(
        default_factory=nauert.MeasurewiseQSchema
    )
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
    simulate_queue(
        sequence,
        tuple(
            voice_specification.note_server
            for voice_specification in voice_specifications
        ),
    )
    for voice_specification in voice_specifications:
        voice_specification.voice.extend(
            nauert.quantize(
                voice_specification.note_server.q_event_sequence,
                voice_specification.q_schema,
                voice_specification.grace_handler,
                voice_specification.heuristic,
                nauert.SerialJobHandler(),
                voice_specification.attack_point_optimizer,
                voice_specification.attach_tempos,
            )
        )
    return QuantizingMetadata()
