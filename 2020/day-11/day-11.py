import itertools


def seat_has_target_value(seats, row_index, column_index, target_value):
    if row_index < 0 or row_index >= len(seats):
        return False
    row = seats[row_index]
    if column_index < 0 or column_index >= len(row):
        return False
    return row[column_index] == target_value


def count_adjacent_seats(seats, row_index, column_index, value):
    rows_to_check = range(row_index - 1, row_index + 2)
    columns_to_check = range(column_index - 1, column_index + 2)
    combinations = set(itertools.product(rows_to_check, columns_to_check))
    combinations.remove((row_index, column_index))
    adjacent_seat_has_value = [
        seat_has_target_value(seats, combination[0], combination[1], value)
        for combination in combinations
    ]
    return sum(adjacent_seat_has_value)


def replace_string_value(string, index, value):
    return string[:index] + value + string[index + 1:]


def print_seats(seats):
    for row in seats:
        print(row, end='')
    print('\n')


def count_seats(seats, value):
    count = 0
    for row in seats:
        for column in row:
            if column == value:
                count += 1

    return count


def execute_seat_rules(seats):
    new_seats = seats.copy()
    change_occurred = False
    for row_index, row in enumerate(seats):
        for column_index, column in enumerate(row):
            if column == EMPTY:
                count = count_adjacent_seats(seats, row_index, column_index, OCCUPIED)
                if count == 0:
                    new_seats[row_index] = replace_string_value(new_seats[row_index], column_index, OCCUPIED)
                    change_occurred = True
            elif column == OCCUPIED:
                count = count_adjacent_seats(seats, row_index, column_index, OCCUPIED)
                if count >= 4:
                    new_seats[row_index] = replace_string_value(new_seats[row_index], column_index, EMPTY)
                    change_occurred = True

    return new_seats, change_occurred


EMPTY = 'L'
FLOOR = '.'
OCCUPIED = '#'

with open('input.txt', 'r') as f:
    ferry_seats = f.readlines()

seats_are_changing = True
while seats_are_changing:
    ferry_seats, seats_are_changing = execute_seat_rules(ferry_seats)

print(count_seats(ferry_seats, OCCUPIED))
