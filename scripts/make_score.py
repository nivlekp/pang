import subprocess

import pang


def main():
    score_directory = pang.get_score_directory()
    args = ["lilypond", "-o", score_directory, score_directory / "score.ly"]
    subprocess.run(args, check=True)


if __name__ == "__main__":
    main()
