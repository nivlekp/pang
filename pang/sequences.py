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

    def _gen_sequence(self):
        self._instances = self._gen_instances()
        self._durations = self._gen_durations()
        self._pitches = self._gen_pitches()

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
    def servers(self):
        return self._servers


class AtaxicCloud(Sequence):
    """
    Ataxic Cloud of sound-points.

    ..  container:: example

        Initializing an ataxic cloud.

        >>> sequence = pang.AtaxicCloud()
        >>> sequence.simulate_queue()
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
        return [random.choice(self._pitch_set) for _ in range(self._number_of_notes)]

    @property
    def arrival_model(self):
        return self._arrival_model

    @property
    def service_model(self):
        return self._service_model
