#!/usr/bin/python

from __future__ import division

import sys
import argparse

class EmptyLineError(ValueError):
    pass

INSTRUCTIONS = ['add', 'subtract', 'multiply', 'divide', 'apply']


def parse_line(line):
    """ parse individual lines from file """

    # strip whitespaces from a line
    line = line.strip()

    if not len(line):
        raise EmptyLineError()

    try:
        instruction, value = line.split(' ')
    except ValueError:
        raise ValueError("valid format: <instruction> <number>")

    try:
        value = int(value)
    except ValueError:
        raise ValueError("instruction number should be an integer")

    if instruction not in INSTRUCTIONS:
        raise ValueError("valid instructions: %s" % (', '.join(INSTRUCTIONS)))

    return instruction, value

def extract_instructions(source):
    """ extract instructions from the file
        source = iterable
    """
    instructions = []
    line_number = 0

    for line in source:
        line_number += 1
        try:
            instruction, number = parse_line(line)
        except EmptyLineError:
            continue
        except ValueError, e:
            raise ValueError("ERROR: invalid instruction on line %i (%s)\n%s" % (line_number, line.strip(), e.message))

        instructions.append((instruction, number))

    return instructions

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