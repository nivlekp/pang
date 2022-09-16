import filecmp

import pytest

import pang


@pytest.mark.parametrize("section_path", pang.get_section_paths())
def test_one_section(section_path):
    music_ly_path = section_path / "music.ly"
    assert music_ly_path.exists()
    music_ly_bak_path = section_path / "music.ly.bak"
    music_ly_path.rename(music_ly_bak_path)

    metadata_json_path = section_path / "__metadata__.json"
    assert metadata_json_path.exists()
    metadata_json_bak_path = section_path / "__metadata__.json.bak"
    metadata_json_path.rename(metadata_json_bak_path)

    pang.build.run_music_py(section_path)

    new_music_ly_path = section_path / "new_music.ly"
    music_ly_path.rename(new_music_ly_path)
    music_ly_bak_path.rename(music_ly_path)
    assert filecmp.cmp(new_music_ly_path, music_ly_path, shallow=False)
    new_music_ly_path.unlink()

    new_metadata_json_path = section_path / "new___metadata__.json"
    metadata_json_path.rename(new_metadata_json_path)
    metadata_json_bak_path.rename(metadata_json_path)
    assert filecmp.cmp(new_metadata_json_path, metadata_json_path, shallow=False)
    new_metadata_json_path.unlink()
