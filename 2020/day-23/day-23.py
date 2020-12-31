
def move_cups(cup_dict, current_cup_index):
    length = len(cup_dict.keys())
    lowest = min(cup_dict.values())
    highest = max(cup_dict.values())
    current_cup = cup_dict[current_cup_index]

    next_three_indexes = [
        j % length for j in range(current_cup_index + 1, current_cup_index + 4)
    ]
    next_three_cups = [
        cup_dict[i] for i in next_three_indexes
    ]

    # Figure out destination cup.
    dest = cup_dict[current_cup_index] - 1
    while dest in next_three_cups or dest < lowest:
        dest -= 1
        if dest < lowest:
            dest = highest

    # Remove next three cups.
    i = (next_three_indexes[0] + 3) % length
    count = 0
    while count < (length - 3):
        cup_dict[(i - 3) % length] = cup_dict[i]
        i = (i + 1) % length
        count += 1

    # Find where removed cups go.
    dest_index = [k for k, v in cup_dict.items() if v == dest][0]
    dest_next_three_indexes = [
        i % length for i in range(dest_index + 1, dest_index + 4)
    ]

    # Insert removed cups.
    i = (dest_next_three_indexes[0] - 1) % length
    while i != dest_next_three_indexes[0]:
        if i > dest_next_three_indexes[0]:
            cup_dict[i] = cup_dict[(i - 3) % length]
        i = (i - 1) % length
    for i, index in enumerate(dest_next_three_indexes):
        cup_dict[index] = next_three_cups[i]

    # Find cup next to current cup, which might have moved.
    current_cup_index = [k for k, v in cup_dict.items() if v == current_cup][0]
    current_cup_index = (current_cup_index + 1) % length

    return current_cup_index


def print_cups(cup_dict):
    sorted_keys = sorted(cup_dict.keys())
    print(''.join([
        str(cup_dict[k]) for k in sorted_keys
    ]))


# CUPS = '398254716'
# NUMBER_OF_MOVES = 100
CUPS = '926574183'
NUMBER_OF_MOVES = 10


cup_dict = {
    i: int(v)
    for i, v in enumerate(CUPS)
}

current_cup_index = 3

for _ in range(NUMBER_OF_MOVES):
    print_cups(cup_dict)
    print(current_cup_index)
    current_cup_index = move_cups(cup_dict, current_cup_index)
    print_cups(cup_dict)
    print('\n')
