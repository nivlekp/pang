import bisect
import itertools
from collections.abc import Iterable

from .soundpointsgenerators import SoundPoint, SoundPointsGenerator


class Sequence:
    """
    Sequence of sound-points.
    """

    def __init__(
        self,
        sound_points: list[SoundPoint],
        sequence_duration: float,
    ):
        self._sound_points = sound_points
        if any(
            s0.instance > s1.instance
            for s0, s1 in itertools.pairwise(self._sound_points)
        ):
            raise ValueError("Sound points are out of order")
        if sound_points and sound_points[-1].instance > sequence_duration:
            raise ValueError("The last sound point starts after the sequence ended")
        self._sequence_duration = sequence_duration

    def __getitem__(self, index) -> SoundPoint:
        return self._sound_points[index]

    def __eq__(self, sequence):
        return (
            self._sound_points == sequence._sound_points
            and self._sequence_duration == sequence._sequence_duration
        )

    def __len__(self):
        return len(self._sound_points)

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return f"{type(self).__name__}(sound_points={self._sound_points!r}, sequence_duration={self._sequence_duration!r})"

    def __iter__(self):
        yield from self._sound_points

    def extend(self, sequence: "Sequence", time_gap=0) -> None:
        """
        Extends a sequence with another.

        ..  container:: example

            >>> instances = [0, 1, 2, 3]
            >>> durations = [0.5, 0.5, 0.5, 0.5]
            >>> sound_points_generator = pang.ManualSoundPointsGenerator(
            ...     instances=instances,
            ...     durations=durations,
            ... )
            >>> sequence_0 = pang.Sequence.from_sound_points_generator(
            ...     sound_points_generator, 4
            ... )
            >>> sequence_1 = pang.Sequence.from_sound_points_generator(
            ...     sound_points_generator, 4
            ... )
            >>> sequence_0.extend(sequence_1)
            >>> print(sequence_0.instances)
            [0, 1, 2, 3, 4, 5, 6, 7]

            >>> print(sequence_0.durations)
            [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

        """
        assert isinstance(sequence, type(self))
        offset = self._sequence_duration + time_gap
        self._sound_points.extend(
            [
                SoundPoint.from_sound_point(
                    sound_point, instance=sound_point.instance + offset
                )
                for sound_point in sequence
            ]
        )
        self._sequence_duration += sequence._sequence_duration + time_gap

    def insert(self, offset: float, sequence: "Sequence") -> None:
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
            >>> sequence_0 = pang.Sequence.from_sound_points_generator(
            ...     sound_points_generator, 4
            ... )
            >>> pitches = [1, 1, 1, 1]
            >>> sound_points_generator = pang.ManualSoundPointsGenerator(
            ...     instances=instances,
            ...     durations=durations,
            ...     pitches=pitches,
            ... )
            >>> sequence_1 = pang.Sequence.from_sound_points_generator(
            ...     sound_points_generator, 4
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
        index = bisect.bisect_left(self.instances, offset)
        self._sound_points[index:] = [
            SoundPoint.from_sound_point(
                sound_point, instance=sound_point.instance + sequence._sequence_duration
            )
            for sound_point in self._sound_points[index:]
        ]
        self._sound_points[index:index] = [
            SoundPoint.from_sound_point(
                sound_point, instance=sound_point.instance + offset
            )
            for sound_point in sequence
        ]
        self._sequence_duration += sequence._sequence_duration

    def superpose(self, offset: float, sequence: "Sequence"):
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
            >>> sequence_0 = pang.Sequence.from_sound_points_generator(
            ...     sound_points_generator, 4
            ... )
            >>> pitches = [1, 1, 1, 1]
            >>> sound_points_generator = pang.ManualSoundPointsGenerator(
            ...     instances=instances,
            ...     durations=durations,
            ...     pitches=pitches,
            ... )
            >>> sequence_1 = pang.Sequence.from_sound_points_generator(
            ...     sound_points_generator, 4
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
        for sound_point in sequence:
            new_instance = sound_point.instance + offset
            index = bisect.bisect_left(self.instances, new_instance)
            self._sound_points.insert(
                index, SoundPoint.from_sound_point(sound_point, instance=new_instance)
            )

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
    def sequence_duration(self):
        """
        Returns the sequence duration in seconds.
        """
        return self._sequence_duration

    @classmethod
    def from_sequences(cls, sequences: Iterable["Sequence"]) -> "Sequence":
        current_duration = 0.0
        sound_points: list[SoundPoint] = []
        for sequence in sequences:
            sound_points.extend(
                [
                    SoundPoint.from_sound_point(
                        sound_point, instance=sound_point.instance + current_duration
                    )
                    for sound_point in sequence
                ]
            )
            current_duration += sequence._sequence_duration
        return cls(sound_points, current_duration)

    @classmethod
    def from_sound_points_generator(
        cls, sound_points_generator: SoundPointsGenerator, sequence_duration: float
    ) -> "Sequence":
        assert isinstance(sound_points_generator, SoundPointsGenerator)
        return cls(sound_points_generator(sequence_duration), sequence_duration)

    @classmethod
    def empty_sequence(cls) -> "Sequence":
        return cls([], 0)
