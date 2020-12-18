import itertools
import copy


def get_cube_is_active(cubes, x, y, z):
    try:
        return cubes[z][y][x] == '#'
    except IndexError:
        return False


def count_active_neighbors(cubes, x, y, z):
    prods = set(itertools.product(
        range(x - 1, x + 2),
        range(y - 1, y + 2),
        range(z - 1, z + 2)
    ))
    prods.remove((x, y, z))

    return sum([
        get_cube_is_active(cubes, x2, y2, z2)
        for (x2, y2, z2) in prods
    ])


def print_cubes(cubes):
    for z in cubes:
        for y in z:
            print(y)
        print('\n')


def count_active_cubes(cubes):
    active_sum = 0
    for z in cubes:
        for y in z:
            active_sum += y.count('#')

    return active_sum


def simulate_cycle(cubes, dimensions=3):
    warp = len(cubes)
    depth = len(cubes[0])
    height = len(cubes[0][0])
    width = len(cubes[0][0][0])

    cubes = [
        [
            [
                '.{}.'.format(cubes[z - 1][y - 1]) if (0 < z <= depth and 0 < y <= height and 0) else
                ''.join(['.' for _ in range(width + 2)])
                for y in range(height + 2)
            ] for z in range(depth + 2)
        ] for w in range((warp + 2 if dimensions == 4 else 1))
    ]
    new_cubes = copy.deepcopy(cubes)

    for z in range(depth + 2):
        for y in range(height + 2):
            for x in range(width + 2):
                is_active = get_cube_is_active(cubes, x, y, z)
                active_neighbors = count_active_neighbors(cubes, x, y, z)
                row = new_cubes[z][y]

                if is_active:
                    new_value = '#' if active_neighbors in [2, 3] else '.'

                else:
                    new_value = '#' if active_neighbors == 3 else '.'

                new_row = row[:x] + new_value + row[x + 1:]
                new_cubes[z][y] = new_row

    return new_cubes


with open('input.txt', 'r') as f:
    cubes = [
        line.split('\n')[0] for line in f.readlines()
    ]

CYCLES_TO_SIMULATE = 6

# Part 1
cubes = [cubes.copy()]
for _ in range(CYCLES_TO_SIMULATE):
    cubes = simulate_cycle(cubes)

print(count_active_cubes(cubes))

# Part 2
cubes = [[cubes.copy]]
for _ in range(CYCLES_TO_SIMULATE):
    cubes = simulate_cycle(cubes, dimensions=4)
