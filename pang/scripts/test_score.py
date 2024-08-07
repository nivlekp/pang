import tempfile

import pang


def test_score():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = pang.build.score(tmpdir)
        assert output_file.exists()
