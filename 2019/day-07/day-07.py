from intcode_computer import IntcodeComputer
from itertools import permutations


def get_linear_system_output(phase_settings, memory):
    last_output = 0
    for phase_setting in phase_settings:
        inputs = [phase_setting, last_output]
        intcode_computer = IntcodeComputer(memory, inputs)
        intcode_computer.run()
        last_output = intcode_computer.get_outputs()[0]

    return last_output


with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

# Part 1
outputs = map(lambda x: get_linear_system_output(x, origin_memory), permutations(range(5)))
print(max(outputs))
