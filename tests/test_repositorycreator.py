import pathlib
import tempfile

from pang.templates import repositorycreator


def test_make_new_repository__successful():
    with tempfile.TemporaryDirectory() as directory:
        repositorycreator.make_new_repository(
            pathlib.Path(directory), "composition", "lorem ipsum"
        )
        assert (pathlib.Path(directory) / "composition").is_dir()
