#!/usr/bin/env python
import os
import sys
import filecmp
import argparse
import colorama
import itertools

colorama.init()


def green(s):
    return colorama.Fore.GREEN + s + colorama.Fore.RESET


def red(s):
    return colorama.Fore.RED + s + colorama.Fore.RESET


def iter_dirs(rootdir):
    elements = (os.path.join(rootdir, el) for el in os.listdir(rootdir))
    dirs = filter(lambda x: os.path.isdir(x), elements)

    for d in dirs:
        yield d
        for sd in iter_dirs(d):
            yield sd


def iter_files(dir_, types=None):
    elements = (os.path.join(dir_, f) for f in os.listdir(dir_))
    files = filter(lambda x: os.path.isfile(x), elements)
    if types is None:
        return files
    else:
        return filter(lambda x: x.endswith(types), files)


def _filecmp(filename, filenames, shallow=False):
    for fn in filenames:
        if (not filename == fn) and filecmp.cmp(filename, fn, shallow=shallow):
            yield fn


def iter_dupes(files, shallow=False):
    done = []
    files = list(files)
    for filename in files:
        dupes = list(_filecmp(filename, files, shallow))
        done.extend(dupes)
        if filename not in done and len(dupes):
            yield dupes + [filename]


def process_arguments(args):
    parser = argparse.ArgumentParser(description="Find duplicate files.")

    # directory
    parser.add_argument('directory',
                        type=str,
                        default='.',
                        help='directory to find duplicates')

    # filetypes
    parser.add_argument('-t', '--filetypes',
                        type=str,
                        default=None,
                        help=('only list file with these endings, '
                              'separated by comma (e.g.: mp3,m4a)'))

    # list
    parser.add_argument('-l', '--list',
                        help='only list dupes',
                        action='store_true')

    # recursive
    parser.add_argument('-r',
                        dest='recursive',
                        help='recursively search all subdirectories',
                        action='store_true')

    # verbose
    parser.add_argument('-v', '--verbose',
                        help='verbose output',
                        action='store_true')

    # shallow
    parser.add_argument('-s', '--shallow',
                        help='use shallow file comparison (may be faster, but '
                              ' less relyable)',
                        action='store_true')

    return parser.parse_args(args)


if __name__ == "__main__":
    args = process_arguments(sys.argv[1:])
    dirs = [args.directory]

    types = None
    if args.filetypes is not None:
        types = tuple([s.strip() for s in args.filetypes.split(',')])

    if args.recursive:
        dirs = itertools.chain(iter(dirs), iter_dirs(args.directory))

    if args.list:
        for d in dirs:
            dupes = list(iter_dupes(iter_files(d, types), args.shallow))
            if len(dupes):
                print(green("Found {} dupes in directory {}:".format(
                    len(dupes), os.path.relpath(d, args.directory))))
                for files in dupes:
                    print([os.path.basename(f) for f in files])
    else:
        for d in dirs:
            dupes = list(iter_dupes(iter_files(d, types), args.shallow))
            if len(dupes):
                print(red("Found {} dupes in directory {}:".format(
                    len(dupes), os.path.relpath(d, args.directory))))

                for i, files in enumerate(dupes, 1):
                    print(green("Dupe {} of {}:".format(i, len(dupes))))
                    for nr, f in enumerate(files, 1):
                        print("{}: {}".format(
                            nr, os.path.basename(f)
                        ))
                    for inp in input("Delete file(s) with nr: ").split():
                        nr = int(inp)
                        f = files[nr - 1]
                        os.remove(f)
                        print(red("{} ...deleted".format(
                            os.path.relpath(f, args.directory))))
            else:
                if args.verbose:
                    print(green("{}...no dupes".format(
                        os.path.relpath(d, args.directory))))