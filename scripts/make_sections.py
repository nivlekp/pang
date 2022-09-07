import argparse
import subprocess

import pang


def _make_one_section(section_path):
    args = ["python", str(section_path / "definition.py")]
    subprocess.run(args)


def main(sections):
    section_paths = pang.get_section_paths(sections)
    for section_path in section_paths:
        print(f"Making Section {section_path.stem}...")
        _make_one_section(section_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make sections")
    parser.add_argument("--sections", action="extend", nargs="+", type=str)
    args = parser.parse_args()
    main(args.sections)
