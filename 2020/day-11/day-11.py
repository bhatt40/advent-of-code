
def get_value_at_location(seats, row_index, column_index):
    if row_index < 0 or row_index >= len(seats):
        return None
    row = seats[row_index]
    if column_index < 0 or column_index >= len(row):
        return None

    return row[column_index]


def direction_has_value(seats, row_index, column_index, direction, value, max_distance):
    distance = 0
    y = row_index
    x = column_index
    while True:
        if max_distance is not None and distance >= max_distance:
            break

        x += direction[0]
        y += direction[1]

        v = get_value_at_location(seats, y, x)
        if not v:
            break

        if v == FLOOR:
            distance += 1
            continue

        return v == value

    return False


def count_adjacent_seats(seats, row_index, column_index, target_value, max_distance):
    DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    direction_has_target_value = [
        direction_has_value(seats, row_index, column_index, direction, target_value, max_distance)
        for direction in DIRECTIONS
    ]

    return sum(direction_has_target_value)


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


def execute_seat_rules(seats, max_adjacents, max_distance=None):
    new_seats = seats.copy()
    change_occurred = False
    for row_index, row in enumerate(seats):
        for column_index, column in enumerate(row):
            if column == EMPTY:
                count = count_adjacent_seats(seats, row_index, column_index, OCCUPIED, max_distance)
                if count == 0:
                    new_seats[row_index] = replace_string_value(new_seats[row_index], column_index, OCCUPIED)
                    change_occurred = True
            elif column == OCCUPIED:
                count = count_adjacent_seats(seats, row_index, column_index, OCCUPIED, max_distance)
                if count >= max_adjacents:
                    new_seats[row_index] = replace_string_value(new_seats[row_index], column_index, EMPTY)
                    change_occurred = True

    return new_seats, change_occurred


def execute_rules_until_stable(seats, max_distance, max_adjacents):
    seats_are_changing = True
    while seats_are_changing:
        seats, seats_are_changing = execute_seat_rules(seats, max_distance=max_distance, max_adjacents=max_adjacents)

    return seats


EMPTY = 'L'
FLOOR = '.'
OCCUPIED = '#'

with open('input.txt', 'r') as f:
    ferry_seats = f.readlines()

# Part 1
seats = execute_rules_until_stable(ferry_seats.copy(), max_distance=1, max_adjacents=4)
print(count_seats(seats, OCCUPIED))

# Part 2
seats = execute_rules_until_stable(ferry_seats.copy(), max_distance=None, max_adjacents=5)
print(count_seats(seats, OCCUPIED))
