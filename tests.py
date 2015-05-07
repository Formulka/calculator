#!/usr/bin/python

import unittest

from calc import extract_instructions, parse_line, EmptyLineError, ExtractionError


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

def main():
    unittest.main()

if __name__ == '__main__':
    main()