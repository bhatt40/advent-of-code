from intcode_computer import execute_intcode_instructions

with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

# Part 1
inputs = (1, -99)
part_1_memory = origin_memory.copy()
output = execute_intcode_instructions(part_1_memory, inputs)
print(output)

# Part 2
inputs = (5, -99)
part_2_memory = origin_memory.copy()
output = execute_intcode_instructions(part_2_memory, inputs)
print(output)
