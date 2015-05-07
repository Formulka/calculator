#!/usr/bin/python

from __future__ import division

import sys
import argparse


# parse individual lines from file
def parse_line(line):
    pass

# extract instructions from the file
def extract_instructions(f):
    pass


def main(args=None):
    usage='%(prog)s <filepath> [-v]'
    description='Simple calculator.'

    parser = argparse.ArgumentParser(usage=usage, description=description)
    parser.add_argument('filepath', action='store', help='source file path')

    pargs = parser.parse_args(args)

    # open the provided file path
    try:
        f = open(pargs.filepath, 'r')
    except (OSError, IOError):
        sys.exit("ERROR: please provide a valid file path")

    f.close()



if __name__ == "__main__":
    main()