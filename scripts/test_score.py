import subprocess
import tempfile

import pytest

import pang


def test_score(score_pdf):
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = pang.build.score(tmpdir)
        assert output_file.exists()
