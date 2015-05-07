#!/usr/bin/python

import unittest

from calc import extract_instructions, parse_line, EmptyLineError, ExtractionError, calculate_instruction,\
    calculate_instructions


class CalcTests(unittest.TestCase):

    def test_parse_line(self):
        # test OK case
        self.assertEquals(parse_line("add 5"), ("add", 5))

        # test whitespaces
        self.assertEquals(parse_line("subtract 4\n"), ("subtract", 4))

        # test invalid value
        with self.assertRaises(ValueError):
            parse_line("add foo")

        # test invalid format
        with self.assertRaises(ValueError):
            parse_line("add 5 5")

        # test invalid instruction
        with self.assertRaises(ValueError):
            parse_line("foo 5")

        # test empty line
        with self.assertRaises(EmptyLineError):
            parse_line("")

        # test float
        with self.assertRaises(ValueError):
            parse_line("add 3.5")

    def test_extract_instructions(self):
        source_base = """
        add 5
        subtract 2
        %s
        add 3
        apply 5
        """
        source = source_base % "divide 5"

        # test OK case
        source_iterable = source.split('\n')
        result = [("add", 5), ("subtract", 2), ("divide", 5), ("add", 3), ("apply", 5)]
        self.assertEquals(extract_instructions(source_iterable), result)

        # test invalid value
        source = source_base % "add foo"
        source_iterable = source.split('\n')
        with self.assertRaises(ValueError):
            extract_instructions(source_iterable)

        # test invalid format
        source = source_base % "add 5 5"
        source_iterable = source.split('\n')
        with self.assertRaises(ValueError):
            extract_instructions(source_iterable)

        # test invalid instruction
        source = source_base % "foo 5"
        source_iterable = source.split('\n')
        with self.assertRaises(ValueError):
            extract_instructions(source_iterable)

        # test empty source
        source = ""
        source_iterable = source.split('\n')
        with self.assertRaises(ExtractionError):
            extract_instructions(source_iterable)

        # test source without terminal instruction
        source_base = """
        add 5
        subtract 2
        add 3
        """
        source_iterable = source.split('\n')
        source_iterable.pop()
        with self.assertRaises(ExtractionError):
            extract_instructions(source_iterable)

    def test_calculate_instruction(self):
        # test addition
        self.assertEquals(calculate_instruction("add", 2, 5), 7)

        # test subtraction
        self.assertEquals(calculate_instruction("subtract", 2, 4), -2)

        # test mutliplication
        self.assertEquals(calculate_instruction("multiply", 8, 9), 72)

        # test division
        self.assertEquals(calculate_instruction("divide", 8, 3), 2.6666666666666665)

        # test zero division
        with self.assertRaises(ZeroDivisionError):
            calculate_instruction("divide", 4, 0)

        # test invalid instruction
        with self.assertRaises(ValueError):
            calculate_instruction("foo", 2, 5)

        # test modulo
        self.assertEquals(calculate_instruction("mod", 5, 4), 1)

        # test power
        self.assertEquals(calculate_instruction("pow", 4, 6), 4096.0)

        # test overflow case
        with self.assertRaises(OverflowError):
            calculate_instruction("pow", 2, 10000)

        # test logarithm
        self.assertAlmostEquals(calculate_instruction("log", 3, 2), 1.5849625007211563)

        # test logarithm of a negative number
        with self.assertRaises(ValueError):
            calculate_instruction("log", -2, 10)


    def test_calculate_instructions(self):
        input_instructions = [
            ("add", 10),
            ("subtract", 5),
            ("multiply", 3),
            ("divide", 2),
            ("apply", 2),
        ]
        original_input_instructions = list(input_instructions)

        # test OK input
        self.assertEquals(calculate_instructions(input_instructions), 10.5)

        # test calculation doesn't change the input_instructions
        self.assertEquals(input_instructions, original_input_instructions)

        # test division by zero exception
        err_input_instructions = list(original_input_instructions)
        err_input_instructions[3] = ("divide", 0)
        with self.assertRaises(ZeroDivisionError):
            calculate_instructions(err_input_instructions)

        # test overflow exception
        err_input_instructions = list(original_input_instructions)
        err_input_instructions[3] = ("pow", 1000000)
        with self.assertRaises(OverflowError):
            calculate_instructions(err_input_instructions)


def main():
    unittest.main()

if __name__ == '__main__':
    main()