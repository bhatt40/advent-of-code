import itertools
import copy


def get_cube_is_active(cubes, x, y, z, w):
    try:
        return cubes[w][z][y][x] == '#'
    except IndexError:
        return False


def count_active_neighbors(cubes, x, y, z, w, dimensions):
    warp_range = [w] if dimensions == 3 else range(w - 1, w + 2)

    prods = set(itertools.product(
        range(x - 1, x + 2),
        range(y - 1, y + 2),
        range(z - 1, z + 2),
        warp_range
    ))
    prods.remove((x, y, z, w))

    return sum([
        get_cube_is_active(cubes, x2, y2, z2, w2)
        for (x2, y2, z2, w2) in prods
    ])


def print_cubes(cubes, dimensions=3):
    if dimensions == 3:
        cubes = cubes[0]

    for z in cubes:
        for y in z:
            print(y)
        print('\n')


def count_active_cubes(cubes):
    active_sum = 0
    for w in cubes:
        for z in w:
            for y in z:
                active_sum += y.count('#')

    return active_sum


def simulate_cycle(cubes, dimensions=3):
    warp = len(cubes)
    depth = len(cubes[0])
    height = len(cubes[0][0])
    width = len(cubes[0][0][0])

    new_warp = warp + 2 if dimensions == 4 else warp
    new_depth = depth + 2
    new_height = height + 2
    new_width = width + 2

    new_warp_indexes = {0, new_warp - 1} if dimensions == 4 else {}
    new_depth_indexes = {0, new_depth - 1}
    new_height_indexes = {0, new_height - 1}

    cubes = [
        [
            [
                ''.join(['.' for _ in range(new_width)]) if (w in new_warp_indexes or z in new_depth_indexes or y in new_height_indexes) else
                '.{}.'.format(cubes[w - 1][z - 1][y - 1]) if dimensions == 4 else
                '.{}.'.format(cubes[w][z - 1][y - 1])
                for y in range(new_height)
            ] for z in range(new_depth)
        ] for w in range(new_warp)
    ]

    new_cubes = copy.deepcopy(cubes)

    for w in range(new_warp):
        for z in range(new_depth):
            for y in range(new_height):
                for x in range(new_width):
                    is_active = get_cube_is_active(cubes, x, y, z, w)
                    active_neighbors = count_active_neighbors(cubes, x, y, z, w, dimensions)
                    row = new_cubes[w][z][y]

                    if is_active:
                        new_value = '#' if active_neighbors in [2, 3] else '.'

                    else:
                        new_value = '#' if active_neighbors == 3 else '.'

                    new_row = row[:x] + new_value + row[x + 1:]
                    new_cubes[w][z][y] = new_row

    return new_cubes


with open('input.txt', 'r') as f:
    original_cubes = [
        line.split('\n')[0] for line in f.readlines()
    ]

CYCLES_TO_SIMULATE = 6

# Part 1
cubes = [[original_cubes.copy()]]
for _ in range(CYCLES_TO_SIMULATE):
    cubes = simulate_cycle(cubes)

print(count_active_cubes(cubes))

# Part 2
cubes = [[original_cubes.copy()]]
for _ in range(CYCLES_TO_SIMULATE):
    cubes = simulate_cycle(cubes, dimensions=4)

print(count_active_cubes(cubes))
