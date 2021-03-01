import random

import numpy as np

import abjad


class SoundPointsGenerator:
    """
    Abstract base sound-point generator.
    """

    def __call__(self, sequence_duration):
        raise NotImplementedError

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()


class AtaxicSoundPointsGenerator(SoundPointsGenerator):
    """
    Ataxic sound-point generator.
    """

    def __init__(
        self,
        arrival_rate=1,
        service_rate=1,
        pitch_set=[0],
        arrival_model="markov",
        service_model="markov",
        seed=123456,
    ):
        self._arrival_rate = arrival_rate
        self._service_rate = service_rate
        self._pitch_set = pitch_set
        self._arrival_model = arrival_model
        self._service_model = service_model
        self._seed = seed

    def __call__(self, sequence_duration):
        np.random.seed(self._seed)
        random.seed(self._seed)
        self._number_of_notes = round(sequence_duration * self._arrival_rate)
        durations = self._gen_durations()
        instances = self._gen_instances()
        pitches = self._gen_pitches()
        return (instances, durations, pitches)

    def _gen_durations(self):
        if self._service_model == "markov":
            return np.random.exponential(1 / self._service_rate, self._number_of_notes)
        elif self.service_model == "deterministic":
            return np.array([1 / self._service_rate] * self._number_of_notes)
        else:
            raise Exception

    def _gen_instances(self):
        if self._arrival_model == "markov":
            instances = np.random.uniform(
                0.0, self._sequence_duration, self._number_of_notes
            )
            return sorted(instances)
        elif self.arrival_model == "deterministic":
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


class ManualSoundPointsGenerator(SoundPointsGenerator):
    """
    Manual sound-point generator.
    """

    def __init__(
        self,
        instances=[0],
        durations=[1],
        pitches=None,
    ):
        assert len(instances) == len(durations)
        if pitches is None:
            pitches = [0] * len(instances)
        assert len(instances) == len(pitches)
        self._instances = instances
        self._durations = durations
        self._pitches = pitches

    def __call__(self, sequence_duration):
        return (self._instances, self._durations, self._pitches)
