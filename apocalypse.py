#!/usr/bin/env python
"""
apocalypse.py

Remove all private data from pc.

"""

import os
import argparse


# all my secret files go in here
targets = [
]


parser = argparse.ArgumentParser(
    description='Remove all private data from this computer.'
)

parser.add_argument(
    '-a', '--all', action='store_true',
    help='process without confirmation'
)

parser.add_argument(
    '--dry', action='store_true',
    help='dryrun'
)


def try_delete(filename):
    res = False
    try:
        os.remove(filename)
    except FileNotFoundError as e:
        print('File "{}"...not found'.format(filename))
    except Exception as e:
        print(e)
    else:
        print('File "{}"...deleted'.format(filename))
        res = True
    return res


def delete_data(dryrun, confirm=True):
    for target in targets:
        if dryrun:
            print('File "{}"'.format(target), end='')
            if os.path.isfile(target):
                print('...found')
            else:
                print('...not found')
            continue

        if confirm:
            res = input('Delete file "{}" (Y/n/a)?'.format(target))

            if res.lower() in ('y', 'a', ''):
                try_delete(target)

            if res.lower() == 'a':
                confirm = False
        else:
            try_delete(target)

if __name__ == '__main__':
    args = parser.parse_args()
    delete_data(args.dry, not args.all)
