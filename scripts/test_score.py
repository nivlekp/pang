import subprocess

import pang


def test_score():
    score_directory = pang.get_score_directory()
    score_pdf = score_directory / "score.pdf"
    new_score_pdf = score_directory / "new_score.pdf"
    score_pdf.rename(new_score_pdf)
    args = ["make", "score"]
    subprocess.run(args, check=True)
    assert score_pdf.exists()
