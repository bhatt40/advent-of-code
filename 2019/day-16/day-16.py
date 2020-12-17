
def get_next_input(input, input_length):
    counter = 0
    index = 0
    while counter < input_length:
        x = input[index]
        i = index
        counter += 1
        index = (index + 1) % len(input)
        yield i, x


def get_element_pattern(base_pattern, position):
    pattern = [
        [x for _ in range(position)]
        for x in base_pattern
    ]
    return [item for sublist in pattern for item in sublist]


def calculate_element_value(input, pattern, input_length):
    pattern_index = 1
    input_index = 0
    element = 0
    repeated_inputs = get_next_input(input, input_length)
    try:
        while True:
            element += next(repeated_inputs)[1] * pattern[pattern_index]
            input_index += 1
            pattern_index = (pattern_index + 1) % len(pattern)
    except StopIteration:
        pass

    return abs(element) % 10


def execute_phase(input, base_pattern, input_length):
    output = [
        calculate_element_value(input, get_element_pattern(base_pattern, index + 1), input_length)
        for index, value in get_next_input(input, input_length)
    ]

    return output


def execute_phase_with_shortcut(input):
    # Based on pattern that occurs.

    def get_next_value(input):
        input_sum = sum(input)
        index = 0
        while index < len(input):
            v = input_sum % 10
            input_sum -= input[index]
            index += 1
            yield v

    return [
        x for x in get_next_value(input)
    ]


with open('input.txt', 'r') as f:
    input = [
        int(x) for x in f.readline().split('\n')[0]
    ]

offset = int(''.join([str(x) for x in input[:7]]))

NUMBER_OF_REPEATS = 10000
NUMBER_OF_PHASES = 100
BASE_PATTERN = [0, 1, 0, -1]

# Part 1
output = input.copy()
input_length = len(output)
for x in range(NUMBER_OF_PHASES):
    output = execute_phase(output, BASE_PATTERN, input_length)

print(''.join([
    str(x) for x in output[:8]
]))

# Part 2

length_of_shortcut_input = (len(input) * NUMBER_OF_REPEATS) - offset
first_index = offset % len(input)
shortcut_input = input[first_index:]
rest_of_shortcut_input = [
    x[1] for x in get_next_input(input, length_of_shortcut_input - len(shortcut_input))
]
output = [
    *shortcut_input,
    *rest_of_shortcut_input
]

for x in range(NUMBER_OF_PHASES):
    output = execute_phase_with_shortcut(output)
    print(x)

print(''.join([
    str(x) for x in output[:8]
]))
