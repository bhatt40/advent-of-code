import re


def deal_new_stack(d, size):
    return {
        (size - pos - 1): card
        for pos, card in d.items()
    }


def cut_n_cards(d, n, size):
    if n >= 0:
        return {
            pos: d[pos + n] if pos < (size - n) else d[(pos + n - size)]
            for pos, card in d.items()
        }

    n = abs(n)
    return {
        pos: d[pos - n] if pos >= n else d[pos + (size - n)]
        for pos, card in d.items()
    }


def deal_with_increment_n(d, n, size):
    i = 0
    i2 = 0
    d2 = {}
    while len(d2.keys()) < size:
        d2[i2] = d[i]
        i2 = (i2 + n) % size
        i += 1

    return d2


def perform_operation(deck, operation_string, size):
    if operation_string == 'deal into new stack':
        return deal_new_stack(deck, size)

    m = re.match(r'^cut (?P<n>-?[0-9]+$)$', operation_string)
    if m:
        n = int(m.group('n'))
        return cut_n_cards(deck, n, size)

    m = re.match(r'^deal with increment (?P<n>[0-9]+)$', operation_string)
    if m:
        n = int(m.group('n'))
        return deal_with_increment_n(deck, n, size)

    raise Exception('Unrecognized operation: {}'.format(operation_string))


def print_deck(d, size):
    print(','.join([
        str(d[x]) for x in range(size)
    ]))


def find_card(d, target):
    for pos, card in d.items():
        if card == target:
            return pos

    return None


with open('input.txt', 'r') as f:
    operation_strings = [
        line.split('\n')[0]
        for line in f.readlines()
    ]

# Part 1
# DECK_SIZE = 10007
#
# deck = {
#     x: x for x in range(DECK_SIZE)
# }
#
# for operation_string in operation_strings:
#     deck = perform_operation(deck, operation_string, DECK_SIZE)
#
# print(find_card(deck, 2019))

# Part 2
DECK_SIZE = 119315717514047

# Modular deck: (offset, increment)
mod_deck = (0, 1)

for operation_string in operation_strings:
    deck = perform_operation(deck, operation_string, DECK_SIZE)

print(deck[2020])
