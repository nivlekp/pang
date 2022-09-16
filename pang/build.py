import json
import subprocess

import abjad


def _get_lilypond_includes():
    return ["../../stylesheets/stylesheet.ily"]


def _get_empty_beatspan(score):
    max_empty_beatspan = abjad.Duration(0)
    for staff in score:
        for voice in staff:
            empty_beatspan = abjad.Duration(0)
            for leaf in abjad.iterate.leaves(voice, reverse=True):
                if isinstance(leaf, abjad.Rest):
                    empty_beatspan += leaf.written_duration
                else:
                    break
            if empty_beatspan > max_empty_beatspan:
                max_empty_beatspan = empty_beatspan
    return max_empty_beatspan


def _get_last_metronome_mark(score):
    last_leaf = abjad.get.leaf(score, -1)
    prototype = abjad.MetronomeMark
    return abjad.get.effective(last_leaf, prototype)


def _get_last_time_signature(score):
    last_leaf = abjad.get.leaf(score, -1)
    prototype = abjad.TimeSignature
    return abjad.get.effective(last_leaf, prototype)


def _collect_metadata(score):
    metadata = {}
    last_metronome_mark = _get_last_metronome_mark(score)
    duration = last_metronome_mark.reference_duration
    reference_duration = f"{duration.numerator}/{duration.denominator}"
    units_per_minute = last_metronome_mark.units_per_minute
    metadata["last_metronome_mark"] = {
        "reference_duration": reference_duration,
        "units_per_minute": units_per_minute,
    }
    time_signature = _get_last_time_signature(score)
    time_signature = f"{time_signature.numerator}/{time_signature.denominator}"
    metadata["last_time_signature"] = time_signature
    duration = _get_empty_beatspan(score)
    metadata["empty_beatspan"] = f"{duration.numerator}/{duration.denominator}"
    return metadata


def make_lilypond_file(score):
    includes = _get_lilypond_includes()
    items = ["#(ly:set-option 'relative-includes #t)"]
    items += [rf'\include "{include}"' for include in includes]
    items += [score]
    lilypond_file = abjad.LilyPondFile(items=items)
    return lilypond_file


def persist(lilypond_file, lilypond_file_path):
    with open(lilypond_file_path, "w") as fp:
        string = abjad.lilypond(lilypond_file)
        fp.write(string)


def run_music_py(section_path):
    path = section_path / "definition.py"
    path = path if path.exists() else section_path / "music.py"
    args = ["python", path]
    subprocess.run(args, check=True)


def section(score, scope, command):
    target = score[scope.voice_name]
    command(target)
    metadata = _collect_metadata(score)
    return metadata


def write_metadata(metadata, file_path):
    with open(file_path, "w") as fp:
        json.dump(metadata, fp)
