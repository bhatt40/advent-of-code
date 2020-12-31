import time


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

    # Insert removed cups after destination cup.
    dest_index = cups.index(dest)
    cups = cups[:dest_index + 1] + next_three_cups + cups[dest_index + 1:]

    # Find cup next to current cup, which might have moved.
    current_cup_index = cups.index(current_cup)
    current_cup_index = (current_cup_index + 1) % length

    return cups, current_cup_index


def move_cups_with_dict(cups, current_cup, lowest, highest):

    next_three_cups = [
        cups[current_cup], cups[cups[current_cup]], cups[cups[cups[current_cup]]]
    ]

    # Figure out destination cup.
    dest = current_cup - 1
    while dest in next_three_cups or dest < lowest:
        dest -= 1
        if dest < lowest:
            dest = highest

    # Remove next three cups.
    cups[current_cup] = cups[cups[cups[cups[current_cup]]]]

    # Insert removed cups after destination cup.
    cup_after_dest = cups[dest]
    cups[dest] = next_three_cups[0]
    cups[next_three_cups[2]] = cup_after_dest

    # Find cup next to current cup, which might have moved.
    current_cup = cups[current_cup]

    return current_cup


def print_cups(cups):
    print(''.join([
        str(v) for v in cups
    ]))


def print_cups_with_dict(cups):
    i = 0
    current = 1
    vs = [
        None for _ in range(len(cups.keys()))
    ]
    while i < len(vs):
        vs[i] = current
        current = cups[current]
        i += 1

    print(''.join([
        str(v) for v in vs
    ]))


# Part 1
CUPS = '398254716'
NUMBER_OF_MOVES = 1000

cups = [
    int(v) for v in CUPS
]

current_cup_index = 0

for _ in range(NUMBER_OF_MOVES):
    cups, current_cup_index = move_cups(cups, current_cup_index)

print_cups(cups)

# Part 2
CUPS = '398254716'
NUMBER_OF_MOVES = 10000000

cups = {}
for index, cup in enumerate(CUPS):
    try:
        next_cup = int(CUPS[index + 1])
    except IndexError:
        next_cup = 10
    cups[int(cup)] = next_cup

for c in range(10, 1000000):
    cups[c] = c + 1
cups[1000000] = int(CUPS[0])

current_cup = int(CUPS[0])

lowest = min(cups.keys())
highest = max(cups.keys())

for i in range(NUMBER_OF_MOVES):
    current_cup = move_cups_with_dict(cups, current_cup, lowest, highest)

print(cups[1] * cups[cups[1]])
