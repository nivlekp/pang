import dataclasses
import random
import typing

import numpy as np

import abjad


@dataclasses.dataclass
class SoundPoint:
    """
    SoundPoint / Event.
    """
    instance: float
    duration: float
    pitch: float | tuple[float]
    attachments: typing.Optional[list[typing.Any]] = None

    def attach(self, attachment):
        if self.attachments is None:
            self.attachments = []
        self.attachments.append(attachment)


class SoundPointsGenerator:
    """
    Abstract base sound-point generator.
    """

    def __call__(self, sequence_duration):
        np.random.seed(self._seed)
        random.seed(self._seed)
        self._number_of_notes = round(sequence_duration * self._arrival_rate)
        for char in self._order:
            if char == "i":
                instances = self._gen_instances(sequence_duration)
            if char == "d":
                durations = self._gen_durations()
            if char == "p":
                pitches = self._gen_pitches()
        return [SoundPoint(i, d, p) for i, d, p in zip(instances, durations, pitches)]

    def _gen_durations(self):
        """
        Generates durations.
        """
        # Since a number of SoundPointsGenerators would probably use this
        # method, it is currently located in the base class.
        assert hasattr(self, "_service_model")
        assert hasattr(self, "_number_of_notes")
        if self._service_model == "markov":
            return np.random.exponential(1 / self._service_rate, self._number_of_notes)
        elif self._service_model == "deterministic":
            return np.array([1 / self._service_rate] * self._number_of_notes)
        else:
            raise Exception

    def _gen_instances(self, sequence_duration):
        """
        Generates durations.
        """
        # Since a number of SoundPointsGenerators would probably use this
        # method, it is currently located in the base class.
        assert hasattr(self, "_arrival_model")
        assert hasattr(self, "_number_of_notes")
        if self._arrival_model == "markov":
            instances = np.random.uniform(0.0, sequence_duration, self._number_of_notes)
            return sorted(instances)
        elif self._arrival_model == "deterministic":
            each_duration = sequence_duration / self._number_of_notes
            instances = [i * each_duration for i in range(self._number_of_notes)]
            return np.array(instances)
        else:
            raise Exception


class AtaxicSoundPointsGenerator(SoundPointsGenerator):
    r"""
    Ataxic sound points generator.

    ..  container:: example

        Initializing an ataxic cloud.

        >>> pitch_set = list(range(24))
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
        >>> optimizer = nauert.MeasurewiseAttackPointOptimizer()
        >>> result = nauert.quantize(
        ...     q_event_sequence, attack_point_optimizer=optimizer
        ... )
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
                    a'8
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
                        f'32
                        ~
                        f'8
                        ~
                    }
                }
                {
                    f'32.
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
        order="idp",
    ):
        self._arrival_rate = arrival_rate
        self._service_rate = service_rate
        self._pitch_set = pitch_set
        self._arrival_model = arrival_model
        self._service_model = service_model
        self._seed = seed
        self._order = order  # For preserving past scores and examples

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
    r"""
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

        >>> sequence.simulate_queue()
        >>> server = sequence.servers[0]
        >>> q_event_sequence = server.q_event_sequence
        >>> optimizer = nauert.MeasurewiseAttackPointOptimizer()
        >>> result = nauert.quantize(
        ...     q_event_sequence, attack_point_optimizer=optimizer
        ... )
        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=60
                    %%% \time 4/4 %%%
                    c'4
                    c'4
                    c'8
                    r8
                    c'8
                    r8
                }
            }

    ..  container:: example

        Initializing a sequence manually with pitches.

        >>> instances = [0, 1, 2, 3]
        >>> durations = [1, 1, 0.5, 0.5]
        >>> pitches = [0, 1, (2, 3), 4]
        >>> sound_points_generator = pang.ManualSoundPointsGenerator(
        ...     instances=instances,
        ...     durations=durations,
        ...     pitches=pitches,
        ... )
        >>> sequence = pang.Sequence(
        ...     sound_points_generator=sound_points_generator,
        ... )
        >>> print(sequence.instances)
        [0, 1, 2, 3]
        >>> print(sequence.durations)
        [1, 1, 0.5, 0.5]
        >>> print(sequence.pitches)
        [0, 1, (2, 3), 4]
        >>> print(sequence.sequence_duration)
        3.5

        >>> sequence.simulate_queue()
        >>> server = sequence.servers[0]
        >>> q_event_sequence = server.q_event_sequence
        >>> optimizer = nauert.MeasurewiseAttackPointOptimizer()
        >>> result = nauert.quantize(
        ...     q_event_sequence, attack_point_optimizer=optimizer
        ... )
        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=60
                    %%% \time 4/4 %%%
                    c'4
                    cs'4
                    <d' ef'>8
                    r8
                    e'8
                    r8
                }
            }
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
        return [
            SoundPoint(i, d, p)
            for i, d, p in zip(self._instances, self._durations, self._pitches)
        ]


class RandomWalkSoundPointsGenerator(SoundPointsGenerator):
    r"""
    Sound points generator, with pitches chosen with a random walk process.

    ..  container:: example

        Initializing an ataxic cloud.

        >>> pitch_set = list(range(20))
        >>> sound_points_generator = pang.RandomWalkSoundPointsGenerator(
        ...     pitch_set=pitch_set,
        ... )
        >>> sequence = pang.Sequence(
        ...     sound_points_generator=sound_points_generator,
        ...     sequence_duration=4,
        ... )
        >>> sequence.simulate_queue()
        >>> server = sequence.servers[0]
        >>> q_event_sequence = server.q_event_sequence
        >>> optimizer = nauert.MeasurewiseAttackPointOptimizer()
        >>> result = nauert.quantize(
        ...     q_event_sequence, attack_point_optimizer=optimizer
        ... )
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
                    bf'8
                    \times 2/3 {
                        \times 4/5 {
                            r32
                            a'16
                            ~
                            a'16
                            ~
                        }
                        \times 2/3 {
                            a'16
                            r8
                        }
                        r8
                    }
                    r4
                    \times 2/3 {
                        r8
                        r16.
                        bf'32
                        ~
                        bf'8
                        ~
                    }
                }
                {
                    bf'32.
                    b'64
                    ~
                    b'16
                    ~
                    b'8
                    ~
                    b'4
                    r2
                }
            }

    """

    def __init__(
        self,
        arrival_rate=1,
        service_rate=1,
        arrival_model="markov",
        service_model="markov",
        pitch_set=[0],
        origin=None,
        seed=123456,
        order="idp",
    ):
        self._arrival_rate = arrival_rate
        self._service_rate = service_rate
        self._arrival_model = arrival_model
        self._service_model = service_model
        self._pitch_set = pitch_set
        if origin is None:
            origin = round(len(pitch_set) / 2)
        assert origin < len(pitch_set) and origin >= 0
        self._origin = origin
        self._seed = seed
        self._order = order

    def _gen_pitches(self):
        """
        Generates pitches using a simple random walk algorithm.
        """
        pitch_set = self._pitch_set
        pitches = []
        index = self._origin
        if self._number_of_notes == 0:
            return pitches
        for i in range(self._number_of_notes):
            pitches.append(pitch_set[index])
            index += random.choice([1, -1])
            if index >= len(pitch_set):
                index = len(pitch_set) - 1
            elif index < 0:
                index = 0
        return pitches


class GRWSoundPointsGenerator(SoundPointsGenerator):
    r"""
    Gaussian (sampled) random walk sound points generator.

    ..  container:: example

        >>> pitch_set = list(range(20))
        >>> sound_points_generator = pang.GRWSoundPointsGenerator(
        ...     pitch_set=pitch_set,
        ... )
        >>> sequence = pang.Sequence(
        ...     sound_points_generator=sound_points_generator,
        ...     sequence_duration=4,
        ... )
        >>> sequence.simulate_queue()
        >>> server = sequence.servers[0]
        >>> q_event_sequence = server.q_event_sequence
        >>> optimizer = nauert.MeasurewiseAttackPointOptimizer()
        >>> result = nauert.quantize(
        ...     q_event_sequence, attack_point_optimizer=optimizer
        ... )
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
                    bf'8
                    \times 2/3 {
                        \times 4/5 {
                            r32
                            bf'16
                            ~
                            bf'16
                            ~
                        }
                        \times 2/3 {
                            bf'16
                            r8
                        }
                        r8
                    }
                    r4
                    \times 2/3 {
                        r8
                        r16.
                        a'32
                        ~
                        a'8
                        ~
                    }
                }
                {
                    a'32.
                    af'64
                    ~
                    af'16
                    ~
                    af'8
                    ~
                    af'4
                    r2
                }
            }


    """

    def __init__(
        self,
        arrival_rate=1,
        service_rate=1,
        arrival_model="markov",
        service_model="markov",
        pitch_set=[0],
        origin=None,
        mean=0,
        standard_deviation=1,
        seed=123456,
        order="idp",
    ):
        self._arrival_rate = arrival_rate
        self._service_rate = service_rate
        self._arrival_model = arrival_model
        self._service_model = service_model
        self._pitch_set = pitch_set
        if origin is None:
            origin = round(len(pitch_set) / 2)
        assert origin < len(pitch_set) and origin >= 0
        self._origin = origin
        self._mean = mean
        self._standard_deviation = standard_deviation
        self._seed = seed
        self._order = order

    def _gen_pitches(self):
        """
        Generates pitches using a round-off normal distribution.
        """
        pitch_set = self._pitch_set
        pitches = []
        index = self._origin
        if self._number_of_notes == 0:
            return pitches
        for i in range(self._number_of_notes):
            pitches.append(pitch_set[index])
            index += round(np.random.normal(self._mean, self._standard_deviation))
            if index >= len(pitch_set):
                index = len(pitch_set) - 1
            elif index < 0:
                index = 0
        return pitches
