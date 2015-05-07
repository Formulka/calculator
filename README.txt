Description:
- script calculates a series of instruction from a file and prints the result on the standard output
- the instructions ignore mathematical precedence and are processed in a series while the last, "apply", instruction provides the input for the first instruction

Requirements:
- script requires python 2.7+


Usage:
python calc.py <filepath> [-o, -i]
filename is a full file path
-o flag outputs individual sub-calculations (optional)
-i flag enables float values in the source file (optional)


Example calls:
python calc.py example.txt
python calc.py -o example.txt
python calc.py -oi example.txt


File format:
<instruction> <number>
<instruction> <number>
<instruction> <number>
...
apply <number>


Valid instructions:
add - adds the number to the input
subtract - subtracts the number from the input
multiply - multiplies the input with the number
divide - divides the input by the number (results in float)
mod - calculates the leftover after dividing the input by the number
pow - calculates the input to the power of the number (results in float)
log - calculates the logarithm to base number of the input (results in float)
apply - the number of this instruction is the first input of the calculation and the instruction is the last one processed


Example input from file:
add 5
subtract 2
multiply 3
apply 4

Example result:
21

Example explanation:
((4 + 5) - 2) * 3 = 21
