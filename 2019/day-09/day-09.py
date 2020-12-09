from intcode_computer import IntcodeComputer

with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

# origin_memory = [109, 1, 203, 2, 204, 2, 99] # Input
# origin_memory = [109, 1, 203, 11, 209, 8, 204, 1, 99, 10, 0, 42, 0]


computer = IntcodeComputer(origin_memory, [10])
computer.run()
print(computer.outputs)
print(computer.is_complete)
