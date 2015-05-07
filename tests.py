#!/usr/bin/python

import unittest

from calc import extract_instructions, parse_line


class CalcTests(unittest.TestCase):

    def test_parse_line(self):
        self.assertEquals(parse_line("add 5"), ("add", 5))

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

        self.assertEquals(extract_instructions(source_iterable), result)

def main():
    unittest.main()

if __name__ == '__main__':
    main()