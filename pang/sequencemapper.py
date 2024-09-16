import dataclasses

import abjad
from abjadext import nauert

from .noteserver import NoteServer
from .queuesimulation import simulate_queue
from .sequences import Sequence


@dataclasses.dataclass(frozen=True)
class QuantizingMetadata:
    number_of_all_discarded_q_events: int
    number_of_discarded_pitched_q_events: int


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
        if voice_specification.note_server.is_empty:
            continue
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
    return _retrieve_quantizing_metadata(voice_specification)


def _retrieve_quantizing_metadata(
    voice_specification: VoiceSpecification,
) -> QuantizingMetadata:
    grace_handler = voice_specification.grace_handler
    match grace_handler:
        case nauert.DiscardingGraceHandler():
            discarded_q_events = grace_handler.discarded_q_events
            return QuantizingMetadata(
                len([event for events in discarded_q_events for event in events]),
                len(
                    [
                        event
                        for events in discarded_q_events
                        for event in events
                        if isinstance(event, nauert.PitchedQEvent)
                    ]
                ),
            )
        case _:
            return QuantizingMetadata(0, 0)
