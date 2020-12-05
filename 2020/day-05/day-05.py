
def get_seat_value(character_set, first_half_character, second_half_character, length):
    seat_value = 0
    for index, character in enumerate(character_set):
        if character == first_half_character:
            pass
        elif character == second_half_character:
            seat_value += (length // (2 ** (index + 1)))
        else:
            raise Exception('Invalid character: {}'.format(character))

    return seat_value


def get_row(character_set):
    return get_seat_value(character_set, ROW_FIRST_HALF_CHARACTER, ROW_SECOND_HALF_CHARACTER, NUMBER_OF_ROWS)


def get_column(character_set):
    return get_seat_value(character_set, COLUMN_FIRST_HALF_CHARACTER, COLUMN_SECOND_HALF_CHARACTER, NUMBER_OF_COLUMNS)


def get_seat_id(row, column):
    return (row * 8) + column


def read_boarding_pass(character_set):
    row_character_set = character_set[0:ROW_CHARACTER_SET_LENGTH]
    row_number = get_row(row_character_set)

    column_character_set = character_set[ROW_CHARACTER_SET_LENGTH: -1]
    column_number = get_column(column_character_set)

    return get_seat_id(row_number, column_number)


def set_has_adjacent_seat_ids(seat_id_set, seat_id):
    return (seat_id + 1) in seat_id_set and (seat_id - 1) in seat_id_set


NUMBER_OF_ROWS = 128
NUMBER_OF_COLUMNS = 8

ROW_FIRST_HALF_CHARACTER = 'F'
ROW_SECOND_HALF_CHARACTER = 'B'

COLUMN_FIRST_HALF_CHARACTER = 'L'
COLUMN_SECOND_HALF_CHARACTER = 'R'

ROW_CHARACTER_SET_LENGTH = 7

with open('input.txt', 'r') as f:
    boarding_passes = f.readlines()

seat_id_set = set(map(lambda x: read_boarding_pass(x), boarding_passes))

# Part 1
print(max(seat_id_set))

# Part 2
all_seat_id_set = set(map(lambda x: get_seat_id(x[0], x[1]), [
    [row, column]
    for column in range(NUMBER_OF_COLUMNS)
    for row in range(NUMBER_OF_ROWS)
]))

missing_seat_id_set = all_seat_id_set - seat_id_set

valid_seats = set(filter(lambda x: set_has_adjacent_seat_ids(seat_id_set, x), missing_seat_id_set))
if len(valid_seats) > 1:
    raise Exception('More than one valid seat found.')
elif len(valid_seats) == 0:
    raise Exception('No valid seats found.')

print(valid_seats)
