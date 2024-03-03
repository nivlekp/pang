import argparse
import subprocess

import pang


def main(sections):
    section_paths = pang.get_section_paths(sections)
    for section_path in section_paths:
        print(f"Making Section {section_path.stem}...")
        pang.build.run_music_py(section_path)
        pang.build.run_lilypond_in_segment_directory(section_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make sections")
    parser.add_argument("--sections", action="extend", nargs="+", type=str)
    args = parser.parse_args()
    main(args.sections)
