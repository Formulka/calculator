#!/usr/bin/python

from __future__ import division

import sys
import argparse

class EmptyLineError(ValueError):
    pass

class ExtractionError(ValueError):
    pass


TERMINAL_INSTRUCTION = 'apply'
INSTRUCTIONS = {
    'add': lambda a, b: a + b,
    'subtract': lambda a, b: a - b,
    'multiply': lambda a, b: a * b,
    'divide': lambda a, b: a / b,
    TERMINAL_INSTRUCTION: lambda a, b: a}


def parse_line(line):
    """ parse individual lines from file """

    # strip whitespaces from a line
    line = line.strip()

    # empty line is invalid
    if not len(line):
        raise EmptyLineError()

    # split the line into a pair instruction, value
    try:
        instruction, value = line.split(' ')
    except ValueError:
        raise ValueError("valid format: <instruction> <number>")

    # convert the string value into an integer
    try:
        value = int(value)
    except ValueError:
        raise ValueError("instruction number should be an integer")

    # validate the instruction
    if instruction not in INSTRUCTIONS:
        raise ValueError("valid instructions: %s" % (', '.join(INSTRUCTIONS)))

    return instruction, value

def extract_instructions(source):
    """ extract instructions from the file
        source = iterable
    """
    instructions = []
    line_number = 0
    is_terminated = False

    # cycle the lines from the source
    for line in source:
        line_number += 1
        try:
            instruction, number = parse_line(line)
        except EmptyLineError:
            continue
        except ValueError, e:
            raise ValueError("ERROR: invalid instruction on line %i (%s)\n%s" % (line_number, line.strip(), e.message))

        # add the parsed instruction to the instructions list
        instructions.append((instruction, number))

        # if the instruction is terminal, exit the cycle
        if instruction == TERMINAL_INSTRUCTION:
            is_terminated = True
            break

    # check if any instructions were provided
    if not len(instructions):
        raise ExtractionError("ERROR: no instructions provided")

    # check if instructions are properly terminated
    if not is_terminated:
        raise ExtractionError("ERROR: missing terminal instruction (%s)" % TERMINAL_INSTRUCTION)

    return instructions

def calculate_instruction(instruction, input_value, instruction_value):
    """ calculate a single instruction
        instruction = one of INSTRUCTIONS
        input_value = input value
        instruction_value = instruction value
    """
    return INSTRUCTIONS[instruction](input_value, instruction_value)

def calculate_instructions(instructions):
    """ calculate all instructions
    """

    # the last instruction is the input value
    terminator, input_value = instructions.pop()
    output_value = input_value

    # cycle through and calculate the instructions
    for instruction, value in instructions:
        try:
            output_value = calculate_instruction(instruction, input_value, value)
        except (ZeroDivisionError, ValueError), e:
            raise
        input_value = output_value

    return output_value

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