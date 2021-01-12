from intcode_computer import IntcodeComputer
import functools


def string_to_ascii_array(string):
    return [
        ord(c) for c in string

    ] + [10]


def ascii_array_to_string(array):
    return ''.join([
        chr(x) for x in array
    ])


def survey(commands):
    inputs = functools.reduce(lambda a, b: a + string_to_ascii_array(b), commands, [])

    intcode_computer = IntcodeComputer(origin_memory, inputs)
    intcode_computer.run()
    output = intcode_computer.get_all_outputs()
    try:
        print(ascii_array_to_string(output))
    except ValueError:
        print(output[-1])


with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

# Part 1
commands = [
    'NOT A J',
    'NOT B T',
    'AND D T',
    'OR T J',
    'NOT C T',
    'AND D T',
    'OR T J',
    'WALK'
]

survey(commands)

# Part 2
commands = [
    'NOT A J',
    'NOT B T',
    'OR T J',
    'NOT C T',
    'AND H T',
    'OR T J',
    'AND D J',
    'RUN'
]

survey(commands)
