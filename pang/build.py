import fractions
import json
import pathlib
import subprocess

import abjad

from .paths import get___main___path, get_score_directory
from .sequencemapper import QuantizingMetadata

PYTHON = "python"
LILYPOND = "lilypond"

MUSIC_LY_FILE_NAME = "music.ly"
MUSIC_ILY_FILE_NAME = "music.ily"
MUSIC_PDF_FILE_NAME = "music.pdf"
MUSIC_PY_FILE_NAME = "music.py"
METADATA_FILE_NAME = "__metadata__.json"


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


def collect_metadata(
    score: abjad.Score, quantizing_metadata_dict: dict[str, QuantizingMetadata]
) -> dict:
    metadata = collect_scorewise_metadata(score)
    metadata["per_voice_metadata"] = {
        voice_name: quantizing_metadata.asdict()
        for voice_name, quantizing_metadata in quantizing_metadata_dict.items()
    }
    return metadata


def collect_scorewise_metadata(score):
    metadata = {}
    metadata["duration"] = float(abjad.get.duration(score, in_seconds=True))
    last_metronome_mark = _get_last_metronome_mark(score)
    duration = last_metronome_mark.reference_duration
    reference_duration = f"{duration.numerator}/{duration.denominator}"
    units_per_minute = last_metronome_mark.units_per_minute
    if isinstance(units_per_minute, fractions.Fraction):
        units_per_minute = float(units_per_minute)
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


def _make_lilypond_files(score):
    includes = _get_lilypond_includes()
    items = ["#(ly:set-option 'relative-includes #t)"]
    items += [rf'\include "{include}"' for include in includes]
    items += [rf'\include "{MUSIC_ILY_FILE_NAME}"']
    music_ly_file = abjad.LilyPondFile(items=items)
    music_ily_file = abjad.LilyPondFile(items=[score])
    return music_ly_file, music_ily_file


def _read_previous_metadata():
    path = get___main___path()
    segment_name = path.parent.name
    if segment_name == "a":
        return None
    previous_segment = ord(segment_name) - 1
    previous_segment_name = chr(previous_segment)
    previous_metadata_path = (
        path.parent.parent / previous_segment_name / METADATA_FILE_NAME
    )
    with open(previous_metadata_path, "r") as fp:
        metadata = json.load(fp)
    return metadata


def _write_metadata(metadata, file_path):
    with open(file_path, "w") as fp:
        json.dump(metadata, fp, indent=4)
        fp.write("\n")


def persist(score, metadata):
    music_ly_file, music_ily_file = _make_lilypond_files(score)
    path = get___main___path()
    music_ly_path = path.parent / MUSIC_LY_FILE_NAME
    with open(music_ly_path, "w") as fp:
        string = abjad.lilypond(music_ly_file)
        fp.write(string)
    music_ily_path = path.parent / MUSIC_ILY_FILE_NAME
    with open(music_ily_path, "w") as fp:
        string = abjad.lilypond(music_ily_file)
        fp.write(string)
    metadata_path = path.parent / METADATA_FILE_NAME
    _write_metadata(metadata, metadata_path)


def run_lilypond_in_segment_directory(section_path):
    assert section_path.exists()
    subprocess.run([LILYPOND, MUSIC_LY_FILE_NAME], cwd=section_path, check=True)


def run_music_py(section_path):
    subprocess.run([PYTHON, section_path / MUSIC_PY_FILE_NAME], check=True)


def score(output_directory=None):
    output_directory_path = pathlib.Path(output_directory or get_score_directory())
    subprocess.run(
        [
            LILYPOND,
            "-o",
            output_directory_path,
            get_score_directory() / MUSIC_LY_FILE_NAME,
        ],
        check=True,
    )
    return output_directory_path / MUSIC_PDF_FILE_NAME
