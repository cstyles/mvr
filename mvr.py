#!/usr/bin/env python3

import re
import os
import sys
import argparse
import glob



DESCRIPTION = 'A script to rename batches of files using regular expressions.'



# Command line arguments
def construct_parser(parser):
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



def mvr(argv):
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    construct_parser(parser)
    args = parser.parse_args(sys.argv[1:])
    
    new_files = []
    
    if args.full:
        args.match_regex = '^' + args.match_regex + '$'
    
    # Recursively search directories
    if args.recursive:
        recursive_files = []
        for f in args.files:
            if os.path.isdir(f):
                recursive_files += glob.glob(
                    f'{f}/**',
                    recursive=True,
                )
        
        # Add in recursively found files
        args.files += recursive_files
        
    for f in args.files:
        new_files.append(
            re.sub(args.match_regex, args.rename_regex, f)
        )
    
    # Check for collisions
    # TODO: Add a verbose option that will print out the offending file(s)
    test_set = set(new_files)
    if len(new_files) > len(test_set):
        print('Collision exists in new file names. Aborting...')
        exit(1)
    
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



# Main method
if __name__ == '__main__':
    mvr(sys.argv[1:])
