import abc
import queue
import random

import numpy as np

import abjad

from .noteserver import NoteServer, _get_closest_server


class Sequence:
    """
    Abstract base sequence.
    """

    def __init__(
        self,
        arrival_rate=1,
        service_rate=1,
        nservers=1,
        pitch_set=None,
        sequence_duration=1,
        seed=123456,
    ):
        self._arrival_rate = arrival_rate
        self._service_rate = service_rate
        self._servers = [NoteServer() for _ in range(nservers)]
        if pitch_set is None:
            pitch_set = abjad.PitchSet()
        else:
            assert isinstance(pitch_set, (list, abjad.PitchSet))
        self._pitch_set = pitch_set
        self._sequence_duration = sequence_duration
        self._number_of_notes = round(self._sequence_duration * self._arrival_rate)
        self._seed = seed

    def __len__(self):
        return len(self.durations)

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    def _gen_sequence(self):
        self._instances = self._gen_instances()
        self._durations = self._gen_durations()
        self._pitches = self._gen_pitches()

    def extend(self, sequence, time_gap=0):
        """
        Extends a sequence with another.

        ..  container:: example

            >>> instances = [0, 1, 2, 3]
            >>> durations = [0.5, 0.5, 0.5, 0.5]
            >>> sequence_0 = pang.ManualSequence(
            ...     instances=instances,
            ...     durations=durations,
            ...     sequence_duration=4,
            ... )
            >>> sequence_1 = pang.ManualSequence(
            ...     instances=instances,
            ...     durations=durations,
            ... )
            >>> sequence_0.extend(sequence_1)
            >>> string = abjad.storage(sequence_0)
            >>> print(string)
            pang.ManualSequence(
                instances=[0, 1, 2, 3, 4, 5, 6, 7],
                durations=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                pitches=[0, 0, 0, 0, 0, 0, 0, 0],
                sequence_duration=7.5,
                nservers=1,
                )
        """
        assert isinstance(sequence, (type(self), Sequence))
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

    @abc.abstractmethod
    def _gen_durations(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _gen_instances(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _gen_pitches(self):
        raise NotImplementedError

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
    def number_of_notes(self):
        """
        Returns the number of notes in the cloud.
        """
        return self._number_of_notes

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
        last_offset = max(offsets)
        return max(self._sequence_duration, last_offset)

    @property
    def servers(self):
        """
        Returns the servers that are attached to this sequence.
        """
        return self._servers


class AtaxicCloud(Sequence):
    r"""
    Ataxic Cloud of sound-points.

    ..  container:: example

        Initializing an ataxic cloud.

        >>> pitch_set = list(range(10))
        >>> sequence = pang.AtaxicCloud(
        ...     pitch_set=pitch_set,
        ...     sequence_duration=4,
        ... )
        >>> sequence.simulate_queue()
        >>> server = sequence.servers[0]
        >>> q_event_sequence = server.q_event_sequence
        >>> quantizer = nauert.Quantizer()
        >>> optimizer = nauert.MeasurewiseAttackPointOptimizer()
        >>> result = quantizer(q_event_sequence, attack_point_optimizer=optimizer)
        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=60
                    %%% \time 4/4 %%%
                    r8
                    e'8
                    \times 2/3 {
                        \times 4/5 {
                            r32
                            c'16
                            ~
                            c'16
                            ~
                        }
                        \times 2/3 {
                            c'16
                            r8
                        }
                        r8
                    }
                    r4
                    \times 2/3 {
                        r8
                        r16.
                        d'32
                        ~
                        d'8
                        ~
                    }
                }
                {
                    d'32.
                    c'64
                    ~
                    c'16
                    ~
                    c'8
                    ~
                    c'4
                    r2
                }
            }
    """

    def __init__(
        self,
        arrival_rate=1,
        service_rate=1,
        nservers=1,
        pitch_set=[0],
        sequence_duration=1,
        queue_type="M/M/1",
        rest_threshold=0.0,
        seed=123456,
    ):
        # TODO: get rid of the extra nservers variable
        self._arrival_model, self._service_model, nservers = tuple(
            queue_type.split("/")
        )
        super().__init__(
            arrival_rate=arrival_rate,
            service_rate=service_rate,
            nservers=int(nservers),
            pitch_set=pitch_set,
            sequence_duration=sequence_duration,
            seed=seed,
        )
        # self._rest_threshold = rest_threshold
        np.random.seed(seed)
        random.seed(seed)
        self._gen_sequence()

    def _gen_durations(self):
        if self._service_model == "M":
            return np.random.exponential(1 / self._service_rate, self._number_of_notes)
        elif self.service_model == "D":
            return np.array([1 / self._service_rate] * self._number_of_notes)
        else:
            raise Exception

    def _gen_instances(self):
        if self._arrival_model == "M":
            instances = np.random.uniform(
                0.0, self._sequence_duration, self._number_of_notes
            )
            return sorted(instances)
        elif self.arrival_model == "D":
            each_duration = self._sequence_duration / self._number_of_notes
            instances = [i * each_duration for i in range(self._number_of_notes)]
            return np.array(instances)
        else:
            raise Exception

    def _gen_pitches(self):
        if isinstance(self._pitch_set, list):
            return [
                random.choice(self._pitch_set) for _ in range(self._number_of_notes)
            ]
        else:
            assert isinstance(self._pitch_set, abjad.PitchSet)
            return [
                random.choice(list(self._pitch_set)).number
                for _ in range(self._number_of_notes)
            ]

    @property
    def arrival_model(self):
        return self._arrival_model

    @property
    def service_model(self):
        return self._service_model


class ManualSequence(Sequence):
    """
    Manual Sequence.

    ..  container:: example

        Initializing a sequence manually.

        >>> instances = [0, 1, 2, 3]
        >>> durations = [1, 1, 0.5, 0.5]
        >>> pitches = [0, 0, 0, 0]
        >>> sequence = pang.ManualSequence(
        ...     instances=instances,
        ...     durations=durations,
        ...     pitches=pitches,
        ... )
        >>> string = abjad.storage(sequence)
        >>> print(string)
        pang.ManualSequence(
            instances=[0, 1, 2, 3],
            durations=[1, 1, 0.5, 0.5],
            pitches=[0, 0, 0, 0],
            sequence_duration=3.5,
            nservers=1,
            )
    """

    def __init__(
        self,
        instances=[0],
        durations=[1],
        pitches=None,
        sequence_duration=None,
        nservers=1,
    ):
        assert len(instances) == len(durations)
        if pitches is None:
            pitches = [0] * len(instances)
        assert len(instances) == len(pitches)
        instances.sort()
        self._instances = instances
        self._durations = durations
        self._pitches = pitches
        offsets = [i + d for i, d in zip(instances, durations)]
        last_offset = max(offsets)
        if sequence_duration is None:
            sequence_duration = last_offset
        else:
            sequence_duration = max(sequence_duration, last_offset)
        super().__init__(nservers=nservers, sequence_duration=sequence_duration)
