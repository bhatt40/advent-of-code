
TARGET_SUM = 2020

with open('input.txt', 'r') as f:
    numbers = [
        int(line) for line in f
    ]

# Part 1
numbers_less_than_half = []
numbers_greater_than_or_equal_to_half = []

for number in numbers:
    if number < TARGET_SUM/2:
        numbers_less_than_half.append(number)
    else:
        numbers_greater_than_or_equal_to_half.append(number)

for lesser_number in numbers_less_than_half:
    for greater_number in numbers_greater_than_or_equal_to_half:
        if lesser_number + greater_number == TARGET_SUM:
            print(lesser_number * greater_number)

# Part 2
for first_index, first_number in enumerate(numbers):
    for second_index in range(first_index, len(numbers)):
        for third_index in range(second_index, len(numbers)):
            second_number = numbers[second_index]
            third_number = numbers[third_index]
            if first_number + second_number + third_number == TARGET_SUM:
                print(first_number * second_number * third_number)