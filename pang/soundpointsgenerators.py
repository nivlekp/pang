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
    r"""
    Ataxic sound points generator.

    ..  container:: example

        Initializing an ataxic cloud.

        >>> pitch_set = list(range(10))
        >>> sound_points_generator = pang.AtaxicSoundPointsGenerator(
        ...     pitch_set=pitch_set,
        ... )
        >>> sequence = pang.Sequence(
        ...     sound_points_generator=sound_points_generator,
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
        instances = self._gen_instances(sequence_duration)
        pitches = self._gen_pitches()
        durations = self._gen_durations()
        return (instances, durations, pitches)

    def _gen_durations(self):
        if self._service_model == "markov":
            return np.random.exponential(1 / self._service_rate, self._number_of_notes)
        elif self.service_model == "deterministic":
            return np.array([1 / self._service_rate] * self._number_of_notes)
        else:
            raise Exception

    def _gen_instances(self, sequence_duration):
        if self._arrival_model == "markov":
            instances = np.random.uniform(0.0, sequence_duration, self._number_of_notes)
            return sorted(instances)
        elif self.arrival_model == "deterministic":
            each_duration = sequence_duration / self._number_of_notes
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

    ..  container:: example

        Initializing a sequence manually.

        >>> instances = [0, 1, 2, 3]
        >>> durations = [1, 1, 0.5, 0.5]
        >>> sound_points_generator = pang.ManualSoundPointsGenerator(
        ...     instances=instances,
        ...     durations=durations,
        ... )
        >>> sequence = pang.Sequence(
        ...     sound_points_generator=sound_points_generator,
        ... )
        >>> print(sequence.instances)
        [0, 1, 2, 3]
        >>> print(sequence.durations)
        [1, 1, 0.5, 0.5]
        >>> print(sequence.sequence_duration)
        3.5
    """

    def __init__(
        self,
        instances=[],
        durations=[],
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
