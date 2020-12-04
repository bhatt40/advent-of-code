def read_instruction(instruction):
    opcode = instruction % 100
    new_instruction = instruction // 100
    parameter_count = 3 if opcode in [1, 2, 7, 8] else 2 if opcode in [5, 6] else 1
    parameter_modes = [
        (new_instruction // (10 ** x)) % 10 for x in range(parameter_count)
    ]
    if opcode not in [4, 5, 6]:
        parameter_modes[-1] = 1
    return opcode, parameter_modes


def read_parameters(memory, instruction_index, parameter_modes):
    return [
        memory[memory[instruction_index + index + 1]] if parameter_mode == 0 else memory[instruction_index + index + 1]
        for index, parameter_mode in enumerate(parameter_modes)
    ]


def calculate_target_value(opcode, parameters, next_input):
    if opcode == 1:
        return parameters[0] + parameters[1]
    elif opcode == 2:
        return parameters[0] * parameters[1]
    elif opcode == 3:
        return next_input
    elif opcode == 4:
        return parameters[0]
    elif opcode == 5:
        return parameters[1] if parameters[0] != 0 else None
    elif opcode == 6:
        return parameters[1] if parameters[0] == 0 else None
    elif opcode == 7:
        return 1 if parameters[0] < parameters[1] else 0
    elif opcode == 8:
        return 1 if parameters[0] == parameters[1] else 0

    raise Exception('Invalid opcode: {}'.format(opcode))


def calculate_target_index(opcode, parameters, memory_index):
    if opcode in [1, 2, 7, 8]:
        return parameters[2]
    elif opcode in [5, 6]:
        return memory_index
    return parameters[0]


def write_to_output(opcode, value, output):
    if opcode == 4:
        output.append(value)


def write_to_memory(opcode, memory, index, value):
    if opcode != 4 and value is not None:
        memory[index] = value


def calculate_new_input_index(opcode, input_index):
    if opcode == 3:
        return input_index + 1
    return input_index


def execute_instructions(memory, inputs):
    memory_index = 0
    input_index = 0
    output = []
    while memory_index < len(memory):
        if memory[memory_index] == 99:
            break

        instruction = memory[memory_index]
        opcode, parameter_modes = read_instruction(instruction)
        parameters = read_parameters(memory, memory_index, parameter_modes)

        target_value = calculate_target_value(opcode, parameters, inputs[input_index])
        target_index = calculate_target_index(opcode, parameters, memory_index)

        write_to_output(opcode, target_value, output)
        write_to_memory(opcode, memory, target_index, target_value)

        input_index = calculate_new_input_index(opcode, input_index)

        if memory[memory_index] == instruction:
            memory_index += len(parameters) + 1
        else:
            memory_index = target_value

    return output


with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

# Part 1
inputs = (1, -99)
part_1_memory = origin_memory.copy()
output = execute_instructions(part_1_memory, inputs)
print(output)

# Part 2
inputs = (5, -99)
part_2_memory = origin_memory.copy()
output = execute_instructions(part_2_memory, inputs)
print(output)
