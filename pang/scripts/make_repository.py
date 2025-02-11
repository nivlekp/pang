import argparse
import pathlib

from pang.templates import repositorycreator


def main():
    arguments = make_parser().parse_args()
    repositorycreator.make_new_repository(
        pathlib.Path(arguments.directory), arguments.name
    )


def make_parser():
    parser = argparse.ArgumentParser(description="Make a new repository")
    parser.add_argument("-d", "--directory")
    parser.add_argument("-n", "--name")
    return parser


if __name__ == "__main__":
    main()
