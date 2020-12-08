import re


def parse_instruction(instruction_string):
    m = re.match(r'^(?P<operation>[a-z]{3}) (?P<argument>[0-9\-+]+)(\n)?$', instruction_string)
    operation = m.group('operation')
    argument = int(m.group('argument'))
    return operation, argument


def get_new_instructions(instructions, modified_instruction_index, old_operation, new_operation):
    new_instructions = instructions.copy()
    new_instructions[modified_instruction_index] = \
        new_instructions[modified_instruction_index].replace(old_operation, new_operation)
    return new_instructions


def execute_instruction(operation, argument, instruction_index, accumulator):
    if operation == 'acc':
        accumulator += argument
        instruction_index += 1
    elif operation == 'jmp':
        instruction_index += argument
    elif operation == 'nop':
        instruction_index += 1
    else:
        raise Exception('Invalid operation: {}'.format(operation))

    return instruction_index, accumulator


def test_modification(instructions, modified_instruction_index):
    operation, argument = parse_instruction(instructions[modified_instruction_index])
    new_operation = 'nop' if operation == 'jmp' else 'jmp' if operation == 'nop' else 'acc'
    new_instructions = get_new_instructions(instructions, modified_instruction_index, operation, new_operation)
    try:
        accumulator = run_instructions_until_loop_reached(new_instructions)
    except Exception:
        pass
    else:
        print('Program terminated normally: accumulator = {}'.format(accumulator))


def run_instructions_until_loop_reached(instructions):
    accumulator = 0
    index = 0
    executed_instruction_set = set()

    while index < len(instructions):
        if index in executed_instruction_set:
            raise Exception('Program looped: accumulator = {}'.format(accumulator))
        instruction = instructions[index]
        operation, argument = parse_instruction(instruction)
        executed_instruction_set.add(index)
        index, accumulator = execute_instruction(operation, argument, index, accumulator)

    return accumulator


with open('input.txt', 'r') as f:
    instructions = f.readlines()

# Part 1
accumulator = run_instructions_until_loop_reached(instructions)

# Part 2
for index in range(0, len(instructions)):
    test_modification(instructions, index)
