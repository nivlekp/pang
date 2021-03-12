class Scope:
    """
    Scope.
    """

    __slots__ = "_voice_name"

    def __init__(self, voice_name):
        self._voice_name = voice_name

    @property
    def voice_name(self):
        return self._voice_name
