import difflib
import filecmp
import sys

import pytest

import pang


def print_diff(path0, path1):
    with open(path0, "r") as fp:
        lines0 = fp.readlines()
    with open(path1, "r") as fp:
        lines1 = fp.readlines()
    diff = difflib.context_diff(lines0, lines1, fromfile="generated", tofile="expected")
    sys.stdout.writelines(diff)


@pytest.mark.parametrize("section_path", pang.get_section_paths())
def test_one_section(section_path):
    music_ly_path = section_path / "music.ly"
    assert music_ly_path.exists()
    music_ly_bak_path = section_path / "music.ly.bak"
    music_ly_path.rename(music_ly_bak_path)

    music_ily_path = section_path / "music.ily"
    assert music_ily_path.exists()
    music_ily_bak_path = section_path / "music.ily.bak"
    music_ily_path.rename(music_ily_bak_path)

    metadata_json_path = section_path / "__metadata__.json"
    assert metadata_json_path.exists()
    metadata_json_bak_path = section_path / "__metadata__.json.bak"
    metadata_json_path.rename(metadata_json_bak_path)

    pang.build.run_music_py(section_path)

    new_music_ly_path = section_path / "new_music.ly"
    music_ly_path.rename(new_music_ly_path)
    music_ly_bak_path.rename(music_ly_path)
    assert filecmp.cmp(new_music_ly_path, music_ly_path, shallow=False), print_diff(
        new_music_ly_path, music_ly_path
    )
    new_music_ly_path.unlink()

    new_music_ily_path = section_path / "new_music.ily"
    music_ily_path.rename(new_music_ily_path)
    music_ily_bak_path.rename(music_ily_path)
    assert filecmp.cmp(new_music_ily_path, music_ily_path, shallow=False), print_diff(
        new_music_ily_path, music_ily_path
    )
    new_music_ily_path.unlink()

    new_metadata_json_path = section_path / "new___metadata__.json"
    metadata_json_path.rename(new_metadata_json_path)
    metadata_json_bak_path.rename(metadata_json_path)
    assert filecmp.cmp(
        new_metadata_json_path, metadata_json_path, shallow=False
    ), print_diff(new_metadata_json_path, metadata_json_path)
    new_metadata_json_path.unlink()
