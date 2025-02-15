import dataclasses
import pathlib
import shutil
from collections.abc import Iterator

TEMPLATE_REPOSITORY = pathlib.Path(__file__).parent / "repository"


@dataclasses.dataclass
class Placeholders:
    project_name: str
    composition_title: str
    project_description: str


def make_new_repository(
    parent_directory_path: pathlib.Path, project_name: str, project_description: str
) -> None:
    print(f"making a new directory {project_name} at {parent_directory_path.resolve()}")
    directory_path = parent_directory_path / project_name
    shutil.copytree(TEMPLATE_REPOSITORY, directory_path)
    _replace_placeholders(
        directory_path,
        Placeholders(project_name, project_name.title(), project_description),
    )
    _rename_file_extensions(directory_path)
    _rename_source_directory(directory_path, project_name)


def _replace_placeholders(
    directory_path: pathlib.Path, placeholders: Placeholders
) -> None:
    for file_path in _all_files_in(directory_path):
        print(f"reading {file_path}")
        content = open(file_path, "r").read()
        with open(file_path, "w") as file:
            file.write(_replace_placeholders_in_file_content(content, placeholders))


def _replace_placeholders_in_file_content(
    content: str, placeholders: Placeholders
) -> str:
    for key, value in dataclasses.asdict(placeholders).items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def _rename_source_directory(directory_path: pathlib.Path, project_name: str) -> None:
    (directory_path / "{{project_name}}").rename(directory_path / project_name)


def _rename_file_extensions(directory_path: pathlib.Path) -> None:
    for file_path in _all_files_in(directory_path):
        if file_path.suffix == ".template":
            file_path.rename(file_path.parent / file_path.stem)


def _all_files_in(directory_path: pathlib.Path) -> Iterator[pathlib.Path]:
    for file_path in (path for path in directory_path.rglob("*") if path.is_file()):
        yield file_path
