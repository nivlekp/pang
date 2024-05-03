import pathlib
import shutil

import abjad
import pang


def main():
    (abjad_path,) = abjad.__path__
    scm_directory = pathlib.Path(abjad_path) / "scm"
    stylesheets_contribution_directory = (
        pang.get_stylesheets_directory() / "abjad_contrib"
    )
    stylesheets_contribution_directory.mkdir(exist_ok=True)
    shutil.copytree(
        scm_directory, stylesheets_contribution_directory, dirs_exist_ok=True
    )


if __name__ == "__main__":
    main()
