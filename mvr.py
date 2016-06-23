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
from glob import glob

# counter = 0

# def counter_format(x):
#     x.format(counter)
#     counter += 1
#     return x


del argv[0]

NUM_ARGS = 3

if len(argv) < NUM_ARGS:
    print('Insufficient number of arguments.')
    exit(-1)

FULL_MATCH_MODE = '-f' in argv[3:]
REVERSE_COUNTER = '-r' in argv[3:]

files = glob(argv[0])
new_files = []

for f in files:
    # Uncomment this for full-match mode (need to match entire string)
    #new_files[i] = re.sub(  '^' + argv[-2] + '$',   # match pattern
    new_files.append(re.sub(argv[1],    # match pattern
                            argv[2],    # replace pattern
                            f))         # string

#map(lambda x: counter_format(x), new_files)

#new_files[:] = []

# Check for collisions
test_set = set(new_files)
if len(new_files) > len(test_set):
    print('Collision exists in new file names. Aborting...')
    exit(1)

# Rename the files
# counter = 0
for old, new in zip(files, new_files):
    if old == new:
        continue
    
    # TODO: zfill with log(len(new_files)) or something
    # new.format(counter) # counter feature
    print('"{0}" => "{1}"'.format(old, new))
    os.rename(old, new)
    # counter += 1
