#!/usr/bin/env python3

import re
import os
import sys
import argparse
import glob


DESCRIPTION = 'A script to rename batches of files using regular expressions.'


def construct_parser():
    """Create an object for parsing command line arguments"""
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    # Positional arguments
    parser.add_argument(
        'match_regex',
        type=str,
        help='The regex to use for matching files.',
    )

    parser.add_argument(
        'rename_regex',
        type=str,
        help='The regex to use for renaming files.',
    )

    parser.add_argument(
        'files',
        type=str,
        nargs='+',
        help='The files to rename.',
    )

    # Optional arguments
    parser.add_argument(
        '-f', '--full',
        action='store_true',
        default=False,
        help='Only rename a file if its filepath is fully matched.',
    )

    parser.add_argument(
        '-i', '--prompt',
        action='store_true',
        default=False,
        help='Prompt when trying to overwrite an existing file',
    )

    parser.add_argument(
        '-n', '--dry-run',
        action='store_true',
        default=False,
        help="Print changes but don't actually rename any files.",
    )

    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        default=False,
        help='Recursively search directories for files to rename.',
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        default=False,
        help='Quiet mode.',
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help='Verbose output - NOT IMPLEMENTED',
    )

    return parser


def mvr(argv):
    """Main method; Rename files using regular expressions"""
    parser = construct_parser()
    args = parser.parse_args(sys.argv[1:])

    new_files = []

    if args.full:
        args.match_regex = '^' + args.match_regex + '$'

    # Recursively search directories
    if args.recursive:
        recursive_files = [
            glob.glob(
                f'{f}/**', recursive=True
            ) for f in args.files if os.path.isdir(f)
        ]

        # Add in recursively found files
        args.files += recursive_files

    new_files = [
        re.sub(args.match_regex, args.rename_regex, f) for f in args.files
    ]

    # Check for collisions
    # TODO: Add a verbose option that will print out the offending file(s)
    test_set = set(new_files)
    if len(new_files) > len(test_set):
        print('Collision exists in new file names. Aborting...')
        return 1

    # Rename the files
    for old, new in zip(args.files, new_files):
        if old == new:
            continue

        if not args.quiet:
            print(f'"{old}" => "{new}"')

        if not args.dry_run:
            if args.prompt and os.path.exists(new):
                resp = input(f'overwrite {new}? (y/n [n]) ')
                if resp.lower() == 'y':
                    os.rename(old, new)
                else:
                    print('not overwritten')
            else:
                os.rename(old, new)

    return 0


if __name__ == '__main__':
    try:
        exit(mvr(sys.argv[1:]))
    except KeyboardInterrupt as e:
        print()
        exit(130)
