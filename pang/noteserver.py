import abc

import nauert

from .soundpointsgenerators import SoundPoint


class AbstractNoteServer(abc.ABC):
    """
    Note Server.
    """

    def __init__(self):
        self._durations = []
        self._pitches = []
        self._attachments = []
        self._offset_instance = 0.0

    def serve(self, curr_time: float, sound_point: SoundPoint):
        """
        Serve one note
        """
        # TODO: model rest_threshold
        if curr_time > self._offset_instance:
            self._durations.append(curr_time - self._offset_instance)
            self._pitches.append(None)
            self._attachments.append(())
        self._durations.append(sound_point.duration)
        self._pitches.append(sound_point.pitch)
        self._attachments.append(sound_point.attachments)
        self._offset_instance = curr_time + sound_point.duration

    @abc.abstractmethod
    def can_serve(self, sound_point: SoundPoint) -> bool:
        raise NotImplementedError

    @property
    def attachments(self):
        return self._attachments

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
    def pitches(self):
        return self._pitches

    @property
    def q_event_sequence(self):
        assert len(self._durations) > 0
        return nauert.QEventSequence.from_millisecond_pitch_attachment_tuples(
            tuple(zip(self.durations_in_millisecond, self.pitches, self.attachments))
        )

    @property
    def is_empty(self):
        return len(self._durations) == 0


class NoteServer(AbstractNoteServer):
    def can_serve(self, sound_point: SoundPoint) -> bool:
        return True
