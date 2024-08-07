import argparse

import pang


def main():
    parser = make_parser()
    args = parser.parse_args()
    section_paths = pang.get_section_paths(args.sections)
    for section_path in section_paths:
        print(f"Making Section {section_path.stem}...")
        pang.build.run_music_py(section_path)
        pang.build.run_lilypond_in_segment_directory(section_path)


def make_parser():
    parser = argparse.ArgumentParser(description="Make sections")
    parser.add_argument("--sections", action="extend", nargs="+", type=str)
    return parser


if __name__ == "__main__":
    main()
