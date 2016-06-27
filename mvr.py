#!/usr/bin/env python

####
# mvr
# A wrapper for mv that enables usage of regular expressions.
# SYNTAX: mvr GLOB_PATTERN MATCH_REGEX REPLACE_REGEX OPTIONS
# - GLOB_PATTERN: A string like '*.txt'.
# - MATCH_REGEX: A regex that decides which files to rename.
# - REPLACE_REGEX: A regex that decides how to rename the files.
# - OPTIONS: Things like full-match mode, etc.
####

# TODO:
# - Add modes ('m' for match; 's' for substitute)
# - Add switch for full-match mode
# - Add counter string (i.e., '{0}' in replace_regex maps to an increasing counter)

import re
import os
from sys import argv
import argparse

# counter = 0

# def counter_format(x):
#     # reverse?
#     x.format(counter)
#     counter += 1
#     return x

DESCRIPTION = 'A script to rename batches of files using regexes.'

# Command line arguments
def construct_parser(parser):
    # Positional arguments
    parser.add_argument('match_regex',
        type=str,
        help='The regex to use for matching files.')
    
    parser.add_argument('rename_regex',
        type=str,
        help='The regex to use for renaming files.')
    
    parser.add_argument('files',
        type=str,
        nargs='+',
        help='The files to rename.')
    
    # Optional arguments
    parser.add_argument('-f', '--full',
        type=int,
        help='Only rename files that the regex fully matches.')


parser = argparse.ArgumentParser(description=DESCRIPTION)
construct_parser(parser)
args = parser.parse_args(argv[1:])

new_files = []

for f in args.files:
    # Uncomment this for full-match mode (need to match entire string)
    #new_files[i] = re.sub(  '^' + argv[-2] + '$',   # match pattern
    new_files.append(
        re.sub(args.match_regex, args.rename_regex, f)
    )

#map(lambda x: counter_format(x), new_files)
#new_files[:] = []


# Check for collisions
test_set = set(new_files)
if len(new_files) > len(test_set):
    print('Collision exists in new file names. Aborting...')
    exit(1)

# Rename the files
# counter = 0
for old, new in zip(args.files, new_files):
    print('doit: {0} {1}'.format(old, new))
    if old == new:
        continue
    
    # TODO: zfill with log(len(new_files)) or something
    # new.format(counter) # counter feature
    print('"{0}" => "{1}"'.format(old, new))
    os.rename(old, new)
    # counter += 1
