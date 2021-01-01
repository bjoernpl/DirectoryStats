import argparse
import pathlib
from data.load import Handler
from data.utils import human_bytes
from tqdm import tqdm
import os
from os.path import join, getsize
from multiprocessing import Pool


def analyze(path, full=False):
    handler = Handler(path)
    stats, cache = handler.load()
    files_scanned = 0
    print(f'Analyzing content of {path}')
    if not stats:
        print("This directory has not been analyzed before, so this could take a while.")
        stats["times_analyzed"] = 1
    else:
        stats["times_analyzed"] += 1

    paths = []
    n_dirs = 0
    with tqdm(desc='Reading files', miniters=0, mininterval=0.1) as pbar:
        for dirpath, _, files in os.walk(path):
            n_dirs += 1
            paths += list(map(lambda x: join(dirpath, x), files))
            # file in files:
            #   p = join(dirpath, file)
            #   paths += [p]
            """p = join(dirpath, file)
            if not full and p not in cache:
                files_scanned += 1
                cache[p] = getsize(p)
            elif full:
                files_scanned += 1
                cache[p] = getsize(p)"""
            pbar.update(len(files))

    with Pool(64) as p:
        size_bytes = sum(
            tqdm(
                p.imap_unordered(getsize, paths),
                desc="Scanning files", miniters=0, mininterval=0.1, total=len(paths)
            ))

    #size_bytes = sum(cache.values())
    stats["total_size_bytes"] = size_bytes
    stats["total_size"] = human_bytes(size_bytes)
    stats["amount_files"] = len(paths)
    stats["amount_dirs"] = n_dirs
    handler.save(stats, cache)
    print(f'Files scanned: {files_scanned}')
    for key, value in stats.items():
        print(f'{key.replace("_", " ")} : {value}')


def main(args: argparse.Namespace):
    assert args.path.exists(), f'Directory does not exist: {args.path.absolute()}'
    assert args.path.is_dir(), f'{args.path.absolute} is not a directory'
    analyze(args.path.resolve(), args.full)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get infos on directories and their contents.')
    parser.add_argument('path', type=pathlib.Path, help='The root path of the directory to be analyzed.')
    parser.add_argument('--full', action='store_true',
                        help='Whether or not rescan already scanned files')
    main(parser.parse_args())
