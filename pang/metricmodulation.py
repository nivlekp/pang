import abjad


def metric_modulation_markup(
    previous_metronome_mark: abjad.MetronomeMark,
    current_metronome_mark: abjad.MetronomeMark,
) -> abjad.Markup:
    return abjad.Markup(
        abjad.string.normalize(
            " ".join(
                [
                    r"\markup",
                    r"\tszkiu-metric-modulation",
                    *_rhythm_strings(previous_metronome_mark, current_metronome_mark),
                ]
            )
        )
    )


def _rhythm_strings(
    previous_metronome_mark: abjad.MetronomeMark,
    current_metronome_mark: abjad.MetronomeMark,
) -> tuple[str, str]:
    return "bla", "bla"
