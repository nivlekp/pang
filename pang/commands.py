from abjadext import nauert


class Command:
    """
    Base command class.
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
        attack_point_optimizer=None,
        grace_handler=None,
        search_tree=None,
    ):
        self._sequence = sequence
        attack_point_optimizer = (
            attack_point_optimizer or nauert.MeasurewiseAttackPointOptimizer()
        )
        assert isinstance(attack_point_optimizer, nauert.AttackPointOptimizer)
        self._attack_point_optimizer = attack_point_optimizer
        grace_handler = grace_handler or nauert.ConcatenatingGraceHandler(
            replace_rest_with_final_grace_note=True
        )
        assert isinstance(grace_handler, nauert.GraceHandler)
        self._grace_handler = grace_handler
        search_tree = search_tree or nauert.UnweightedSearchTree()
        assert isinstance(search_tree, nauert.SearchTree)
        self._q_schema = nauert.MeasurewiseQSchema(search_tree=search_tree)
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
                attack_point_optimizer=self._attack_point_optimizer,
                grace_handler=self._grace_handler,
            )
            results.append(result)
        return results
