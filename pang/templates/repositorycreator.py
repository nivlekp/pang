import pathlib
import shutil

TEMPLATE_REPOSITORY = pathlib.Path(__file__).parent / "repository"


def make_new_repository(
    parent_directory_path: pathlib.Path, project_name: str, project_description: str
) -> None:
    print(f"making a new directory {project_name} at {parent_directory_path.resolve()}")
    directory_path = parent_directory_path / project_name
    shutil.copytree(TEMPLATE_REPOSITORY, directory_path)
    _replace_placeholders(directory_path, project_name, project_description)


def _replace_placeholders(
    directory_path: pathlib.Path, project_name: str, project_description: str
) -> None:
    for file_path in directory_path.rglob("*"):
        content = open(file_path, "r").read()
        with open(file_path, "w") as file:
            file.write(
                content.replace("{{project_name}}", project_name).replace(
                    "{{project_description}}", project_description
                )
            )
