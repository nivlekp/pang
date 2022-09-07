import filecmp
import subprocess

import pytest

import pang


@pytest.mark.parametrize("section_path", pang.get_section_paths())
def test_one_section(section_path):
    music_ly_path = section_path / "music.ly"
    assert music_ly_path.exists()
    music_ly_bak_path = section_path / "music.ly.bak"
    music_ly_path.rename(music_ly_bak_path)
    args = ["python", str(section_path / "definition.py")]
    subprocess.run(args)
    new_music_ly_path = section_path / "new_music.ly"
    music_ly_path.rename(new_music_ly_path)
    music_ly_bak_path.rename(music_ly_path)
    assert filecmp.cmp(new_music_ly_path, music_ly_path, shallow=False)