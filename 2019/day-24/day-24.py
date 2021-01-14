
def get_new_value(col, rows, i, j):
    adjacent_bug_count = 0
    for i2, j2 in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
        try:
            adjacent_bug_count += 1 if (i2 >= 0 and j2 >= 0 and rows[i2][j2] == '#') else 0
        except IndexError:
            pass

    if col == '#':
        return '#' if adjacent_bug_count == 1 else '.'

    return '#' if adjacent_bug_count in [1, 2] else '.'


def get_new_3d_value(levels, value, i, j, k):
    adjacency_mappings = {
        # (j, k): [(+i2, j2, k2), ...]
        (0, 0): [(1, 1, 2), (0, 0, 1), (0, 1, 0), (1, 2, 1)],
        (0, 1): [(1, 1, 2), (0, 0, 2), (0, 1, 1), (0, 0, 0)],
        (0, 2): [(1, 1, 2), (0, 0, 3), (0, 1, 2), (0, 0, 1)],
        (0, 3): [(1, 1, 2), (0, 0, 4), (0, 1, 3), (0, 0, 2)],
        (0, 4): [(1, 1, 2), (1, 2, 3), (0, 1, 4), (0, 0, 3)],
        (1, 0): [(0, 0, 0), (0, 1, 1), (0, 2, 0), (1, 2, 1)],
        (1, 1): [(0, 0, 1), (0, 1, 2), (0, 2, 1), (0, 1, 0)],
        (1, 2): [(0, 0, 2), (0, 1, 3), (-1, 0, 0), (-1, 0, 1), (-1, 0, 2), (-1, 0, 3), (-1, 0, 4), (0, 1, 1)],
        (1, 3): [(0, 0, 3), (0, 1, 4), (0, 2, 3), (0, 1, 2)],
        (1, 4): [(0, 0, 4), (1, 2, 3), (0, 2, 4), (0, 1, 3)],
        (2, 0): [(0, 1, 0), (0, 2, 1), (0, 3, 0), (1, 2, 1)],
        (2, 1): [(0, 1, 1), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (-1, 3, 0), (-1, 4, 0), (0, 3, 1), (0, 2, 0)],
        (2, 2): [(0, 1, 2), (0, 2, 3), (0, 3, 2), (0, 2, 1)],
        (2, 3): [(0, 1, 3), (0, 2, 4), (0, 3, 3), (-1, 0, 4), (-1, 1, 4), (-1, 2, 4), (-1, 3, 4), (-1, 4, 4)],
        (2, 4): [(0, 1, 4), (1, 2, 3), (0, 3, 4), (0, 2, 3)],
        (3, 0): [(0, 2, 0), (0, 3, 1), (0, 4, 0), (1, 2, 1)],
        (3, 1): [(0, 2, 1), (0, 3, 2), (0, 4, 1), (0, 3, 0)],
        (3, 2): [(-1, 4, 0), (-1, 4, 1), (-1, 4, 2), (-1, 4, 3), (-1, 4, 4), (0, 3, 3), (0, 4, 2), (0, 3, 1)],
        (3, 3): [(0, 2, 3), (0, 3, 4), (0, 4, 3), (0, 3, 2)],
        (3, 4): [(0, 2, 4), (1, 2, 3), (0, 4, 4), (0, 3, 3)],
        (4, 0): [(0, 3, 0), (0, 4, 1), (1, 3, 2), (1, 2, 1)],
        (4, 1): [(0, 3, 1), (0, 4, 2), (1, 3, 2), (0, 4, 0)],
        (4, 2): [(0, 3, 2), (0, 4, 3), (1, 3, 2), (0, 4, 1)],
        (4, 3): [(0, 3, 3), (0, 4, 4), (1, 3, 2), (0, 4, 2)],
        (4, 4): [(0, 3, 4), (1, 2, 3), (1, 3, 2), (0, 4, 3)]
    }

    if j == 2 and k == 2:
        return '.'

    adjacent_bug_count = 0
    for di2, j2, k2 in adjacency_mappings[j, k]:
        i2 = i + di2
        try:
            adjacent_bug_count += 1 if (i2 >= 0 and j2 >= 0 and k2 >= 0 and levels[i2][j2][k2] == '#') else 0
        except IndexError:
            pass

    if value == '#':
        return '#' if adjacent_bug_count == 1 else '.'

    return '#' if adjacent_bug_count in [1, 2] else '.'


def elapse_minute(rows):
    return [
        ''.join([
            get_new_value(col, rows, i, j) for j, col in enumerate(row)
        ])
        for i, row in enumerate(rows)
    ]


def elapse_3d_minute(levels):
    new_levels = [
        [
            ''.join([
                get_new_3d_value(levels, col, i, j, k)
                for k, col in enumerate(row)
            ])
            for j, row in enumerate(level)
        ]
        for i, level in enumerate(levels)
    ]

    new_inner_level = [
        ''.join([
            get_new_3d_value(levels, '.', -1, j, k)
            for k in range(len(levels[0][0]))
        ])
        for j in range(len(levels[0]))
    ]

    new_outer_level = [
        ''.join([
            get_new_3d_value(levels, '.', len(levels), j, k)
            for k in range(len(levels[0][0]))
        ])
        for j in range(len(levels[0]))
    ]

    new_levels = [
        *([new_inner_level] if not is_empty(new_inner_level) else []),
        *new_levels,
        *([new_outer_level] if not is_empty(new_outer_level) else [])
    ]

    return new_levels


def calc_bio_rating(rows):
    rating = 0
    for i, row in enumerate(rows):
        for j, col in enumerate(row):
            if col == '#':
                x = (len(row) * i) + j
                rating += 2 ** x

    return rating


def print_level(level):
    for row in level:
        print(row)
    print('\n')


def is_empty(level):
    for row in level:
        if '#' in row:
            return False

    return True


def count_bugs(levels):
    count = 0
    for level in levels:
        for rows in level:
            for row in rows:
                for c in row:
                    if c == '#':
                        count += 1

    return count


with open('input.txt', 'r') as f:
    original_rows = [
        row.split('\n')[0] for row in f.readlines()
    ]

# Part 1
ratings = set()
rows = original_rows.copy()
while True:
    rows = elapse_minute(rows)
    rating = calc_bio_rating(rows)
    if rating in ratings:
        break
    ratings.add(rating)

print(rating)

# Part 2
levels = [original_rows.copy()]
minutes_to_run = 200
for _ in range(minutes_to_run):
    levels = elapse_3d_minute(levels)

print(count_bugs(levels))
