from intcode_computer import IntcodeComputer

with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

# Part 1
inputs = [1]
part1_intcode_computer = IntcodeComputer(origin_memory, inputs)
part1_intcode_computer.run()
print(part1_intcode_computer.pop_last_output())

# Part 2
inputs = [5]
part2_intcode_computer = IntcodeComputer(origin_memory, inputs)
part2_intcode_computer.run()
print(part2_intcode_computer.pop_last_output())
