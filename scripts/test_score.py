import subprocess

import pytest

import pang


@pytest.fixture
def score_pdf():
    score_directory = pang.get_score_directory()
    score_pdf = score_directory / "music.pdf"
    expected_score_pdf = score_directory / "expected_music.pdf"
    if score_pdf.exists():
        score_pdf.rename(expected_score_pdf)
    args = ["make", "score"]
    subprocess.run(args, check=True)
    yield score_pdf
    if expected_score_pdf.exists():
        expected_score_pdf.rename(score_pdf)


def test_score(score_pdf):
    assert score_pdf.exists()
