import subprocess

import pang


def test_score():
    score_directory = pang.get_score_directory()
    score_ly = score_directory / "score.ly"
    score_pdf = score_directory / "score.pdf"
    args = ["make", "score"]
    subprocess.run(args, check=True)
    assert score_pdf.exists()
