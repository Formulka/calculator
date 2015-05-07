Tests are located in the test.py file.

To run the tests, run:
python -m test
in the package directory

There is one testcase
CalcTests
with four individual tests
test_parse_line
test_extract_instructions
test_calculate_instruction
test_calculate_instructions

To run an individual test, run:
python -m unittest -v path.to.test
in the package directory

Example of an individual test run:
python -m unittest -v test.CalcTests.test_parse_line