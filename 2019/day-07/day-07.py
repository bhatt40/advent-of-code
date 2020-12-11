from intcode_computer import IntcodeComputer
from itertools import permutations


def get_linear_system_output(phase_settings, memory):
    last_output = 0
    for phase_setting in phase_settings:
        inputs = [phase_setting, last_output]
        intcode_computer = IntcodeComputer(memory, inputs)
        intcode_computer.run()
        last_output = intcode_computer.pop_last_output()

    return last_output


def get_feedback_loop_system_output(phase_settings, memory):
    input_queues = [
        [phase_setting] for index, phase_setting in enumerate(phase_settings)
    ]
    computer_list = [
        IntcodeComputer(memory, input_queues[index]) for index, phase_setting in enumerate(phase_settings)
    ]
    computer_list[0].append_new_input(0)

    current_computer_index = 0
    while not computer_list[-1].is_complete():
        current_computer = computer_list[current_computer_index]
        next_computer_index = (current_computer_index + 1) % len(computer_list)
        next_computer = computer_list[next_computer_index]

        current_computer.run()

        if not next_computer.is_complete():
            new_output = current_computer.pop_last_output()
            if new_output:
                next_computer.append_new_input(new_output)

        current_computer_index = next_computer_index

    return computer_list[-1].pop_last_output()


with open('input.txt', 'r') as f:
    origin_memory = [
        int(x) for x in f.readline().split(',')
    ]

# Part 1
outputs = map(lambda x: get_linear_system_output(x, origin_memory), permutations(range(5)))
print(max(outputs))

# Part 2
outputs = map(lambda x: get_feedback_loop_system_output(x, origin_memory), permutations(range(5, 10)))
print(max(outputs))
