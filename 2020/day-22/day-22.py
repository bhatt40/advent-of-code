from queue import Queue
from copy import copy


def play_round(q1, q2):
    c1 = q1.get()
    c2 = q2.get()

    if c1 > c2:
        q1.put(c1)
        q1.put(c2)
    else:
        q2.put(c2)
        q2.put(c1)


def play_recursive_game(q1, q2, game_number):
    winner = None
    previous_scores = set()
    while not q1.empty() and not q2.empty():
        winner = play_recursive_round(q1, q2, previous_scores, game_number)
        if not winner:
            break

    return winner or 1


def play_recursive_round(q1, q2, previous_scores, game_number):
    print(game_number)
    s1 = calculate_score(q1)
    s2 = calculate_score(q2)
    if (s1, s2) in previous_scores:
        return None
    previous_scores.add((s1, s2))

    c1 = q1.get()
    c2 = q2.get()

    if q1.qsize() >= c1 and q2.qsize() >= c2:
        q1_copy = create_subgame_deck(q1, c1)
        q2_copy = create_subgame_deck(q2, c2)
        winner = play_recursive_game(q1_copy, q2_copy, game_number + 1)
    elif c1 > c2:
        winner = 1
    else:
        winner = 2

    if winner == 1:
        q1.put(c1)
        q1.put(c2)
    elif winner == 2:
        q2.put(c2)
        q2.put(c1)

    return winner


def create_subgame_deck(q, c):
    q_copy = Queue()
    length = q.qsize()
    for _ in range(length):
        v = q.get()
        if c > 0:
            q_copy.put(v)
        q.put(v)
        c -= 1

    return q_copy


def calculate_score(q):
    score = 0
    length = q.qsize()
    count = length
    for _ in range(length):
        v = q.get()
        score += v * count
        q.put(v)
        count -= 1

    return score


q1_original = Queue()
q2_original = Queue()

with open('input.txt', 'r') as f:
    f.readline()
    while True:
        card = f.readline()
        if card in ['', '\n']:
            break
        q1_original.put(int(card))

    f.readline()
    while True:
        card = f.readline()
        if card in ['', '\n']:
            break
        q2_original.put(int(card))


# Part 1
q1 = copy(q1_original)
q2 = copy(q2_original)
while not q1.empty() and not q2.empty():
    play_round(q1, q2)

if q1.empty():
    print(calculate_score(q2))
else:
    print(calculate_score(q1))

# Part 2
q1 = copy(q1_original)
q2 = copy(q2_original)
score_set = set()

winner = play_recursive_game(q1, q2, 0)
if winner == 2:
    print(calculate_score(q2))
else:
    print(calculate_score(q1))

