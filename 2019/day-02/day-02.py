def calculate_target_value(instruction, a, b):
    if instruction == 1:
        return a + b
    elif instruction == 2:
        return a * b
    raise Exception('Invalid instruction: {}'.format(instruction))


def execute_instructions(memory):
    index = 0
    while index < len(memory):
        if memory[index] == 99:
            break
        target_value = calculate_target_value(memory[index], memory[memory[index + 1]], memory[memory[index + 2]])
        memory[memory[index + 3]] = target_value

        index += 4


NOUN_POSITION = 1
VERB_POSITION = 2

with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

# Part 1
memory = origin_memory.copy()
memory[NOUN_POSITION] = 12
memory[VERB_POSITION] = 2

execute_instructions(memory)

print(memory[0])

# Part 2
TARGET_OUTPUT = 19690720

for noun in range(0, 100):
    for verb in range(0, 100):
        memory = origin_memory.copy()
        memory[NOUN_POSITION] = noun
        memory[VERB_POSITION] = verb

        execute_instructions(memory)

        if memory[0] == TARGET_OUTPUT:
            print('Noun: {}'.format(noun))
            print('Verb: {}'.format(verb))
            print('Answer: {}'.format(100 * noun + verb))



