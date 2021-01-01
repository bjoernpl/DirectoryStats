import argparse
import pathlib
from data.load import Handler


def main(args: argparse.Namespace):
    assert args.path.exists(), f'Directory does not exist: {args.path.absolute()}'
    handler = Handler(args.path.absolute())
    stats, cache = handler.load()
    print(f'Analyzing content of {args.path.absolute()}')
    if not stats:
        print("This directory has not been analyzed before, so this could take a while.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get infos on directories and their contents.')
    parser.add_argument('path', type=pathlib.Path, help='The root path of the directory to be analyzed.')
    main(parser.parse_args())

