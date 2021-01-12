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
DECK_SIZE = 10007

deck = {
    x: x for x in range(DECK_SIZE)
}

for operation_string in operation_strings:
    deck = perform_operation(deck, operation_string, DECK_SIZE)

print(find_card(deck, 2019))

# Part 2 - copied from: https://github.com/mcpower/adventofcode/blob/501b66084b0060e0375fc3d78460fb549bc7dfab/2019/22/a-improved.py
cards = 119315717514047
repeats = 101741582076661

# increment = 1 = the difference between two adjacent numbers
# doing the process will multiply increment by increment_mul.
increment_mul = 1
# offset = 0 = the first number in the sequence.
# doing the process will increment this by offset_diff * (the increment before the process started).
offset_diff = 0


def inv(n, cards):
    # gets the modular inverse of n
    # as cards is prime, use Euler's theorem
    return pow(n, cards - 2, cards)


def get(offset, increment, i, cards):
    # gets the ith number in a given sequence
    return (offset + i * increment) % cards


def get_sequence(iterations, increment_mul, offset_diff, cards):
    # calculate (increment, offset) for the number of iterations of the process
    # increment = increment_mul^iterations
    increment = pow(increment_mul, iterations, cards)
    # offset = 0 + offset_diff * (1 + increment_mul + increment_mul^2 + ... + increment_mul^iterations)
    # use geometric series.
    offset = offset_diff * (1 - increment) * inv((1 - increment_mul) % cards, cards)
    offset %= cards
    return increment, offset


for operation_string in operation_strings:
    if operation_string == "deal into new stack":
        # reverse sequence.
        # instead of going up, go down.
        increment_mul *= -1
        increment_mul %= cards
        # then shift 1 left
        offset_diff += increment_mul
        offset_diff %= cards
    elif operation_string.startswith("cut"):
        n = int(re.match(r'^cut (?P<n>-?[0-9]+$)$', operation_string).group('n'))
        # shift n left
        offset_diff += n * increment_mul
        offset_diff %= cards
    elif operation_string.startswith("deal with increment "):
        n = int(re.match(r'^deal with increment (?P<n>[0-9]+)$', operation_string).group('n'))
        # difference between two adjacent numbers is multiplied by the
        # inverse of the increment.
        increment_mul *= inv(n, cards)
        increment_mul %= cards


increment, offset = get_sequence(repeats, increment_mul, offset_diff, cards)
print(get(offset, increment, 2020, cards))
