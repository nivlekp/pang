from abjadext import nauert


class Command:
    """
    Base command class. To be called by SegmentMaker.
    """

    def __call__(self):
        raise NotImplementedError


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

    def __call__(self):
        sequence = self._sequence
        sequence.simulate_queue()
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
        return results
