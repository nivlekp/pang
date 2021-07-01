import bisect
import queue
import typing

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
        if sound_points_generator is None:
            sound_points_generator = ManualSoundPointsGenerator()
        assert isinstance(sound_points_generator, SoundPointsGenerator)
        result = sound_points_generator(sequence_duration)
        self._sound_points = result
        self._sequence_duration = sequence_duration

    def __getitem__(self, index):
        return self._sound_points[index]

    def __len__(self):
        return len(self.sound_points)

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    def __iter__(self):
        yield from self._sound_points

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
        for sound_point in sequence:
            sound_point.instance += offset
        self._sound_points.extend(sequence._sound_points)

    def insert(self, offset, sequence):
        """
        Inserts a sequence into another. ``offset`` should be specified in
        seconds.

        ..  container:: example

            >>> instances = [0, 1, 2, 3]
            >>> durations = [0.5, 0.5, 0.5, 0.5]
            >>> pitches = [0, 0, 0, 0]
            >>> sound_points_generator = pang.ManualSoundPointsGenerator(
            ...     instances=instances,
            ...     durations=durations,
            ...     pitches=pitches,
            ... )
            >>> sequence_0 = pang.Sequence(
            ...     sound_points_generator=sound_points_generator,
            ...     sequence_duration=4,
            ... )
            >>> pitches = [1, 1, 1, 1]
            >>> sound_points_generator = pang.ManualSoundPointsGenerator(
            ...     instances=instances,
            ...     durations=durations,
            ...     pitches=pitches,
            ... )
            >>> sequence_1 = pang.Sequence(
            ...     sound_points_generator=sound_points_generator,
            ...     sequence_duration=4,
            ... )
            >>> sequence_0.insert(2, sequence_1)
            >>> print(sequence_0.instances)
            [0, 1, 2, 3, 4, 5, 6, 7]

            >>> print(sequence_0.pitches)
            [0, 0, 1, 1, 1, 1, 0, 0]

            >>> print(sequence_0.durations)
            [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

        """
        assert isinstance(sequence, type(self))
        # Currently this only supports when the sequences have the same number
        # of servers.
        assert sequence.nservers == self.nservers
        index = bisect.bisect_left(self.instances, offset)
        for sound_point in self._sound_points[index:]:
            sound_point.instance += sequence.sequence_duration
        for sound_point in sequence:
            sound_point.instance += offset
        self._sound_points[index:index] = sequence._sound_points

    def simulate_queue(self):
        """
        Simulate the queue based on the queue type.
        """
        # TODO: model rest_threshold
        assert self.instances is not None and len(self.instances) > 0
        servers = self._servers
        curr_time = 0.0
        q: queue.Queue = queue.Queue()
        arrival_index = 0
        while arrival_index < len(self.instances) or not q.empty():
            server_index, closest_offset_instance = _get_closest_server(servers)
            if q.empty():
                if closest_offset_instance > self.instances[arrival_index]:
                    # previous note has not finished yet, so we should queue
                    # the newly arrived note
                    q.put(arrival_index)
                    curr_time = self.instances[arrival_index]
                    arrival_index = arrival_index + 1
                else:
                    curr_time = self.instances[arrival_index]
                    servers[server_index].serve(
                        curr_time,
                        sound_point=self._sound_points[arrival_index]
                        # duration=self.durations[arrival_index],
                        # pitch=self.pitches[arrival_index]
                    )
                    arrival_index = arrival_index + 1
            else:  # there's already a client in the queue
                # queue the current note
                if (
                    arrival_index < len(self.instances)
                    and closest_offset_instance > self.instances[arrival_index]
                ):
                    q.put(arrival_index)
                    curr_time = self.instances[arrival_index]
                    arrival_index = arrival_index + 1
                else:
                    index = q.get()
                    curr_time = closest_offset_instance
                    servers[server_index].serve(
                        curr_time,
                        sound_point=self._sound_points[index],
                        # duration=self.durations[index],
                        # pitch=self.pitches[index]
                    )

    def superpose(self, offset, sequence):
        """
        Superpose a sequence on top of another. ``offset`` should be specified
        in seconds.

        ..  container:: example

            >>> instances = [0, 1, 2, 3]
            >>> durations = [0.5, 0.5, 0.5, 0.5]
            >>> pitches = [0, 0, 0, 0]
            >>> sound_points_generator = pang.ManualSoundPointsGenerator(
            ...     instances=instances,
            ...     durations=durations,
            ...     pitches=pitches,
            ... )
            >>> sequence_0 = pang.Sequence(
            ...     sound_points_generator=sound_points_generator,
            ...     sequence_duration=4,
            ... )
            >>> pitches = [1, 1, 1, 1]
            >>> sound_points_generator = pang.ManualSoundPointsGenerator(
            ...     instances=instances,
            ...     durations=durations,
            ...     pitches=pitches,
            ... )
            >>> sequence_1 = pang.Sequence(
            ...     sound_points_generator=sound_points_generator,
            ...     sequence_duration=4,
            ... )
            >>> sequence_0.superpose(2, sequence_1)
            >>> print(sequence_0.instances)
            [0, 1, 2, 2, 3, 3, 4, 5]

            >>> print(sequence_0.pitches)
            [0, 0, 1, 0, 1, 0, 1, 1]

            >>> print(sequence_0.durations)
            [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

        """
        assert isinstance(sequence, type(self))
        # Currently this only supports when the sequences have the same number
        # of servers.
        assert sequence.nservers == self.nservers
        for sound_point in sequence:
            sound_point.instance += offset
            index = bisect.bisect_left(self.instances, sound_point.instance)
            self._sound_points.insert(index, sound_point)

    @property
    def instances(self):
        return [event.instance for event in self._sound_points]

    @property
    def pitches(self):
        return [event.pitch for event in self._sound_points]

    @property
    def durations(self):
        return [event.duration for event in self._sound_points]

    @property
    def durations_in_millisecond(self):
        """
        Returns the duration of each note in millisecond (before queue
        simulation).
        """
        return [event.duration * 1000 for event in self._sound_points]

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
        offsets = [i + d for i, d in zip(self.instances, self.durations)]
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
