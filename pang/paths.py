import pathlib


def get_content_directory():
    wrapper_directory = pathlib.Path()
    egg_infos = list(wrapper_directory.glob("*.egg-info"))
    assert len(egg_infos) == 1
    content_directory_name = egg_infos[0].stem
    return wrapper_directory / content_directory_name


def get_section_paths(sections=None):
    content_directory = get_content_directory()
    if sections is not None:
        return [content_directory / "segments" / section for section in sections]
    else:
        paths = sorted((content_directory / "segments").glob("*"))
        return [
            path
            for path in paths
            if path.is_dir()
            and not path.stem.startswith(".")
            and not path.stem.startswith("_")
        ]