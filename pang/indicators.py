import abjad


class Indicator:
    """
    Indicator base class. This is to support attaching indicators before
    quantizing using Nauert.
    """

    def attach(self, target: abjad.LogicalTie):
        raise NotImplementedError
