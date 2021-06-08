from abjadext import nauert

from .indicators import decode


class Command:
    """
    Base command class. To be called by SegmentMaker.
    """

    def __call__(self, target):
        raise NotImplementedError


class DecodeCommand(Command):
    """
    Command to decode indicator.
    """

    def __call__(self, target):
        decode(target)


class QuantizeSequenceCommand(Command):
    """
    Quantize Sequence Command.
    """

    def __init__(
        self,
        sequence,
        q_schema=None,
        grace_handler=None,
        heuristic=None,
        attack_point_optimizer=None,
        attach_tempos=True,
        tag_as_pitch=False,
    ):
        self._sequence = sequence
        self._q_schema = q_schema or nauert.MeasurewiseQSchema()
        self._grace_handler = grace_handler or nauert.ConcatenatingGraceHandler(
            replace_rest_with_final_grace_note=True
        )
        self._heuristic = heuristic or nauert.DistanceHeuristic()
        self._attack_point_optimizer = (
            attack_point_optimizer or nauert.MeasurewiseAttackPointOptimizer()
        )
        self._attach_tempos = attach_tempos
        self._quantizer = nauert.Quantizer()
        self._tag_as_pitch = tag_as_pitch

    def __call__(self, target):
        sequence = self._sequence
        sequence.simulate_queue(tag_as_pitch=self._tag_as_pitch)
        results = []
        for server in sequence.servers:
            q_event_sequence = server.q_event_sequence
            result = self._quantizer(
                q_event_sequence,
                q_schema=self._q_schema,
                grace_handler=self._grace_handler,
                heuristic=self._heuristic,
                attack_point_optimizer=self._attack_point_optimizer,
                attach_tempos=self._attach_tempos,
            )
            results.append(result)
        assert len(results) == 1
        result = results[0]
        target.extend(result)
