#!/usr/bin/python

import unittest

from calc import extract_instructions, parse_line


class CalcTests(unittest.TestCase):

    def test_parse_line(self):
        # test OK case
        self.assertEquals(parse_line("add 5"), ("add", 5))

        # test case with whitespaces
        self.assertEquals(parse_line("subtract 4\n"), ("subtract", 4))

        # test case with invalid value
        with self.assertRaises(ValueError):
            parse_line("add foo")

        # test case with invalid format
        with self.assertRaises(ValueError):
            parse_line("add foo bar")


    def test_extract_instructions(self):
        source = """
        add 5
        subtract 2
        divide 5
        add 3
        apply 5
        """
        source_iterable = source.split('\n')
        result = [("add", 5), ("subtract", 2), ("divide", 5), ("add", 3), ("apply", 5)]

        # test OK case
        self.assertEquals(extract_instructions(source_iterable), result)



def main():
    unittest.main()

if __name__ == '__main__':
    main()