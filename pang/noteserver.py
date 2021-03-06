from abjadext import nauert


def _get_closest_server(servers):
    offset_instance, idx = min(
        (server.offset_instance, idx) for (idx, server) in enumerate(servers)
    )
    return idx, offset_instance


class NoteServer:
    """
    Note Server.
    """

    def __init__(self, rest_threshold=0.0):
        self._durations = []
        self._pitches = []
        self._offset_instance = 0.0
        self._rest_threshold = rest_threshold

    def serve(self, curr_time, duration, pitch):
        """
        Serve one note
        """
        # TODO: model rest_threshold
        if curr_time > self._offset_instance:
            self._durations.append(curr_time - self._offset_instance)
            self._pitches.append(None)
        self._durations.append(duration)
        self._pitches.append(pitch)
        self._offset_instance = curr_time + duration

    @property
    def durations(self):
        return self._durations

    @property
    def durations_in_millisecond(self):
        return [duration * 1000 for duration in self._durations]

    @property
    def offset_instance(self):
        return self._offset_instance

    @property
    def pitch_set(self):
        return self._pitch_set

    @property
    def pitches(self):
        return self._pitches

    @property
    def q_event_sequence(self):
        return nauert.QEventSequence.from_millisecond_pitch_pairs(
            tuple(zip(self.durations_in_millisecond, self.pitches))
        )
