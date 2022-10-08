import pathlib

import __main__
import tomlkit


def get_content_directory():
    wrapper_directory = pathlib.Path()
    egg_infos = list(wrapper_directory.glob("*.egg-info"))
    assert len(egg_infos) <= 1
    if len(egg_infos) == 1:
        content_directory_name = egg_infos[0].stem
    else:
        with open(wrapper_directory / "pyproject.toml", "r") as fp:
            pyproject = tomlkit.load(fp)
        content_directory_name = pyproject["project"]["name"]
    return wrapper_directory / content_directory_name


def get_score_directory():
    content_directory = get_content_directory()
    score_directory = content_directory / "builds" / "score"
    assert score_directory.is_dir()
    return score_directory


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


def get___main___path():
    file = __main__.__file__
    return pathlib.Path(file)
