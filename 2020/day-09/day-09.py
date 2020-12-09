import itertools


def target_sum_exists_in_list(numbers, target_sum):
    combinations = itertools.combinations(numbers, 2)
    sums = [
        combination[0] + combination[1]
        for combination in combinations
    ]
    return target_sum in sums


def find_first_invalid_number(numbers, check_length):
    index = check_length

    while index < len(numbers):
        value = numbers[index]
        check_list = numbers[index - check_length: index]

        if not target_sum_exists_in_list(check_list, value):
            return value

        index += 1

    return None


def find_contiguous_set_that_sums_to_target_value(numbers, target_value):
    for index, number in enumerate(numbers):
        set_index = index
        while set_index < len(numbers):
            set_to_check = numbers[index:set_index + 1]
            sum_of_set = sum(set_to_check)

            if sum_of_set == target_value:
                return set_to_check
            elif sum_of_set > target_value:
                break

            set_index += 1

    return None


CHECK_LENGTH = 25

with open('input.txt', 'r') as f:
    numbers = [
        int(line) for line in f
    ]

first_invalid_number = find_first_invalid_number(numbers, CHECK_LENGTH)

# Part 1
print(first_invalid_number)

found_set = find_contiguous_set_that_sums_to_target_value(numbers, first_invalid_number)
print(min(found_set) + max(found_set))
