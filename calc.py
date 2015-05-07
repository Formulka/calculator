#!/usr/bin/python

from __future__ import division

import sys
import argparse
import math

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
    'mod': lambda a, b: a % b,
    'pow': lambda a, b: math.pow(a, b),
    'log': lambda a, b: math.log(a, b),
    TERMINAL_INSTRUCTION: lambda a, b: a
}

def validate_instruction(instruction):
    """ validate instruction """
    if instruction not in INSTRUCTIONS:
        raise ValueError("invalid instruction (%s), valid instructions: %s" % (instruction, ', '.join(INSTRUCTIONS)))

def parse_line(line, accept_float=False):
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
        if accept_float:
            try:
                value = float(value)
            except:
                raise ValueError("instruction number should be an integer or a float")
        else:
            raise ValueError("instruction number should be an integer")

    # validate the instruction
    validate_instruction(instruction)

    return instruction, value

def extract_instructions(source, accept_float=False):
    """ extract instructions from the file
        source = iterable
    """
    instructions = []
    is_terminated = False

    # cycle the lines from the source
    for line_number, line in enumerate(source, start=1):
        try:
            instruction, number = parse_line(line, accept_float=accept_float)
        except EmptyLineError:
            continue
        except ValueError, e:
            raise ValueError("ERROR: on line %i (%s)\n%s" % (line_number, line.strip(), e.message))

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

    #validate instruction
    validate_instruction(instruction)

    return INSTRUCTIONS[instruction](input_value, instruction_value)

def calculate_instructions(input_instructions, output_instructions=False):
    """ calculate all instructions
    """
    instructions = list(input_instructions)

    # the last instruction is the input value
    terminator, input_value = instructions.pop()
    output_value = input_value

    # cycle through and calculate the instructions
    for instruction, instruction_value in instructions:
        try:
            output_value = calculate_instruction(instruction, input_value, instruction_value)
        except (ZeroDivisionError, ValueError):
            raise
        except OverflowError, e:
            raise OverflowError("overflow, %s" % e.message)

        # print the individual instructions if required
        if output_instructions:
            print "%s %s %s" % (input_value, instruction, instruction_value)

        input_value = output_value

    return output_value

def main(args=None):
    usage='%(prog)s <filepath> [-o]'
    description='Simple calculator.'

    parser = argparse.ArgumentParser(usage=usage, description=description)
    parser.add_argument('filepath', action='store', help='source file path')
    parser.add_argument('-o','--output', action='store_true', help='output the instructions')
    parser.add_argument('-f','--float', action='store_true', help='accept floats in instructions')

    pargs = parser.parse_args(args)

    # open the provided file path
    try:
        f = open(pargs.filepath, 'r')
    except (OSError, IOError):
        sys.exit("ERROR: please provide a valid file path")

    # extract instructions
    try:
        instructions = extract_instructions(f, accept_float=pargs.float)
    except (ValueError, ExtractionError), e:
        f.close()
        sys.exit(e.message)

    f.close()

    # calculate instructions
    try:
        result = calculate_instructions(instructions, pargs.output)
    except (ValueError, ZeroDivisionError, OverflowError), e:
        sys.exit(e.message)

    # print the result
    print result

if __name__ == "__main__":
    main()