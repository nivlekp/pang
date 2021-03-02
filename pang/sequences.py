import queue

import abjad

from .noteserver import NoteServer, _get_closest_server
from .soundpointsgenerators import ManualSoundPointsGenerator, SoundPointsGenerator


class Sequence:
    """
    Sequence of sound-points.
    """

    def __init__(
        self,
        sound_points_generator=None,
        nservers=1,
        sequence_duration=0,
    ):
        self._servers = [NoteServer() for _ in range(nservers)]
        # if pitch_set is None:
        #     pitch_set = abjad.PitchSet()
        # else:
        #     assert isinstance(pitch_set, (list, abjad.PitchSet))
        if sound_points_generator is None:
            sound_points_generator = ManualSoundPointsGenerator()
        assert isinstance(sound_points_generator, SoundPointsGenerator)
        result = sound_points_generator(sequence_duration)
        self._instances, self._durations, self._pitches = result
        self._sequence_duration = sequence_duration

    def __len__(self):
        return len(self.durations)

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    def extend(self, sequence, time_gap=0):
        """
        Extends a sequence with another.

        ..  container:: example

            >>> instances = [0, 1, 2, 3]
            >>> durations = [0.5, 0.5, 0.5, 0.5]
            >>> sound_points_generator = pang.ManualSoundPointsGenerator(
            ...     instances=instances,
            ...     durations=durations,
            ... )
            >>> sequence_0 = pang.Sequence(
            ...     sound_points_generator=sound_points_generator,
            ...     sequence_duration=4,
            ... )
            >>> sequence_1 = pang.Sequence(
            ...     sound_points_generator=sound_points_generator,
            ... )
            >>> sequence_0.extend(sequence_1)
            >>> print(sequence_0.instances)
            [0, 1, 2, 3, 4, 5, 6, 7]

            >>> print(sequence_0.durations)
            [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        """
        assert isinstance(sequence, type(self))
        # Currently this only supports when the sequences have the same number
        # of servers.
        assert sequence.nservers == self.nservers
        offset = self.sequence_duration + time_gap
        new_instances = [i + offset for i in sequence.instances]
        self._instances.extend(new_instances)
        self._durations.extend(sequence.durations)
        self._pitches.extend(sequence.pitches)

    def simulate_queue(self):
        """
        Simulate the queue based on the queue type.
        """
        # TODO: model rest_threshold
        assert self._instances is not None and len(self._instances) > 0
        servers = self._servers
        curr_time = 0.0
        q = queue.Queue()
        arrival_index = 0
        while arrival_index < len(self._instances) or not q.empty():
            server_index, closest_offset_instance = _get_closest_server(servers)
            if q.empty():
                if closest_offset_instance > self._instances[arrival_index]:
                    # previous note has not finished yet, so we should queue
                    # the newly arrived note
                    q.put(arrival_index)
                    curr_time = self._instances[arrival_index]
                    arrival_index = arrival_index + 1
                else:
                    curr_time = self._instances[arrival_index]
                    servers[server_index].serve(
                        curr_time,
                        self._durations[arrival_index],
                        self._pitches[arrival_index],
                    )
                    arrival_index = arrival_index + 1
            else:  # there's already a client in the queue
                # queue the current note
                if (
                    arrival_index < len(self._instances)
                    and closest_offset_instance > self._instances[arrival_index]
                ):
                    q.put(arrival_index)
                    curr_time = self._instances[arrival_index]
                    arrival_index = arrival_index + 1
                else:
                    index = q.get()
                    curr_time = closest_offset_instance
                    servers[server_index].serve(
                        curr_time, self._durations[index], self._pitches[index]
                    )

    def superpose(self, sequence):
        assert isinstance(sequence, type(self))
        # Currently this only supports when the sequences have the same number
        # of servers.
        assert sequence.nservers == self.nservers
        durations = self._durations + sequence.durations
        instances = self._instances + sequence.instances
        pitches = self._pitches + sequence.pitches
        instances_tuple, durations_tuple, pitches_tuple = zip(
            *sorted(zip(instances, durations, pitches))
        )
        self._instances = list(instances_tuple)
        self._durations = list(durations_tuple)
        self._pitches = list(pitches_tuple)

    @property
    def instances(self):
        return self._instances

    @property
    def pitches(self):
        return self._pitches

    @property
    def durations(self):
        return self._durations

    @property
    def durations_in_millesecond(self):
        """
        Returns the duration of each note in millesecond (before queue
        simulation).
        """
        return [dur * 1000 for dur in self._durations]

    @property
    def nservers(self):
        """
        Returns the number of servers.
        """
        return len(self._servers)

    @property
    def sequence_duration(self):
        """
        Returns the sequence duration in seconds.
        """
        offsets = [i + d for i, d in zip(self._instances, self._durations)]
        if offsets != []:
            last_offset = max(offsets)
        else:
            last_offset = 0
        return max(self._sequence_duration, last_offset)

    @property
    def servers(self):
        """
        Returns the servers that are attached to this sequence.
        """
        return self._servers
