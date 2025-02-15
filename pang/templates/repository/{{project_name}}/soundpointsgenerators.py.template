import numpy as np
import pang

REPEADTED_NOTE_WEIGHT_MULTIPLIER = 0.1


class SoundPointsGenerator(pang.SoundPointsGenerator):
    def __init__(
        self,
        note_durations: tuple[float, ...],
        note_duration_distribution: tuple[float, ...],
        phrase_mean_duration: float,
        phrase_minimum_duration: float,
        rest_mean_duration: float,
        pitches_set: set[int],
        seed: int,
    ) -> None:
        if len(note_durations) != len(note_duration_distribution):
            raise ValueError(
                "note durations and their distribution should be of the same length"
            )
        if sum(note_duration_distribution) != 1.0:
            raise ValueError("note duration distribution should sum up to 1")
        self._note_durations = note_durations
        self._note_duration_distribution = note_duration_distribution
        self._phrase_mean_duration = phrase_mean_duration
        self._phrase_minimum_duration = phrase_minimum_duration
        self._rest_mean_duration = rest_mean_duration
        self._pitches_set = pitches_set
        self._random_number_generator = np.random.default_rng(seed)

    def __call__(self, sequence_duration: float) -> list[pang.SoundPoint]:
        first_phrase_start = self._random_number_generator.uniform(
            0.0, self._rest_mean_duration
        )
        duration = first_phrase_start
        sound_points: list[pang.SoundPoint] = []
        while duration < sequence_duration:
            phrase_duration = (
                self._random_number_generator.exponential(
                    self._phrase_mean_duration - self._phrase_minimum_duration
                )
                + self._phrase_minimum_duration
            )
            if phrase_duration + duration >= sequence_duration:
                break
            sound_points.extend(
                [
                    pang.SoundPoint.from_sound_point(
                        sound_point, instance=sound_point.instance + duration
                    )
                    for sound_point in _generate_phrase(
                        self._note_durations,
                        self._note_duration_distribution,
                        self._pitches_set,
                        phrase_duration,
                        self._random_number_generator,
                    )
                ]
            )
            duration = (
                sound_points[-1].instance
                + sound_points[-1].duration
                + self._rest_mean_duration
            )
        return sound_points


def _generate_phrase(
    durations: tuple[float, ...],
    note_duration_distribution: tuple[float, ...],
    pitches_set: set[int],
    sequence_duration: float,
    random_number_generator: np.random.Generator,
) -> list[pang.SoundPoint]:
    current_duration = 0.0
    sound_points: list[pang.SoundPoint] = []
    pitch: int | None = None
    while current_duration < sequence_duration:
        note_duration = random_number_generator.choice(
            durations, p=note_duration_distribution
        )
        if current_duration + note_duration >= sequence_duration:
            break
        pitch = _generate_next_pitch(pitch, pitches_set, random_number_generator)
        sound_points.append(pang.SoundPoint(current_duration, note_duration, pitch))
        current_duration += note_duration
    return sound_points


def _generate_next_pitch(
    pitch: int | None,
    pitches_set: set[int],
    random_number_generator: np.random.Generator,
) -> int:
    if pitch is None:
        return int(random_number_generator.choice(list(pitches_set)))
    weights = np.exp(-np.abs(np.array(pitches_set) - pitch) / 2.0)
    weights[np.array(pitches_set) == pitch] *= REPEADTED_NOTE_WEIGHT_MULTIPLIER
    return int(
        random_number_generator.choice(list(pitches_set), p=weights / weights.sum())
    )
