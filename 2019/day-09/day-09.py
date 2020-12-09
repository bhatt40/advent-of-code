from intcode_computer import IntcodeComputer

with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

# Part 1
computer = IntcodeComputer(origin_memory, [1])
computer.run()
print(computer.pop_last_output())

# Part 2
computer = IntcodeComputer(origin_memory, [2])
computer.run()
print(computer.pop_last_output())
