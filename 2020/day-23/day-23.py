
def move_cups(cups, current_cup_index):
    length = len(cups)
    lowest = min(cups)
    highest = max(cups)
    current_cup = cups[current_cup_index]

    next_three_indexes = [
        j % length for j in range(current_cup_index + 1, current_cup_index + 4)
    ]
    next_three_cups = [
        cups[i] for i in next_three_indexes
    ]

    # Figure out destination cup.
    dest = cups[current_cup_index] - 1
    while dest in next_three_cups or dest < lowest:
        dest -= 1
        if dest < lowest:
            dest = highest

    # Remove next three cups.
    for cup in next_three_cups:
        cups.remove(cup)

    # Find where removed cups go.
    dest_index = cups.index(dest)
    cups = cups[:dest_index + 1] + next_three_cups + cups[dest_index + 1:]

    # Find cup next to current cup, which might have moved.
    current_cup_index = cups.index(current_cup)
    current_cup_index = (current_cup_index + 1) % length

    return cups, current_cup_index


def print_cups(cups):
    print(''.join([
        str(v) for v in cups
    ]))


# Part 1
CUPS = '398254716'
NUMBER_OF_MOVES = 100

cups = [
    int(v) for v in CUPS
]

current_cup_index = 0

for _ in range(NUMBER_OF_MOVES):
    cups, current_cup_index = move_cups(cups, current_cup_index)

print_cups(cups)

# Part 2
