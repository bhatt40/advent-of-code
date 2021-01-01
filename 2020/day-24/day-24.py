from collections import Counter


def get_neighbors(location):
    return {
        location + 1, location - 1, location + 0.5 + 1j, location + 0.5 - 1j, location - 0.5 + 1j, location - 0.5 - 1j
    }


def flip_tiles(black_tiles):
    tx = [ t.real for t in black_tiles ]
    ty = [ t.imag for t in black_tiles ]
    new_black_tiles = set()

    miny = min(ty)
    maxy = max(ty)
    minx = min(tx)
    maxx = max(tx)

    y = miny - 1
    while y <= maxy + 1:
        x = minx - 1
        if (y % 2 == 0 and x % 1 == 0.5) or (y % 2 == 1 and x % 1 == 0):
            x -= 0.5

        while x <= maxx + 1:
            l = complex(x, y)
            is_black = l in black_tiles
            black_neighbor_count = len(list(filter(lambda n: n in black_tiles, get_neighbors(l))))
            if (is_black and black_neighbor_count in [1, 2]) or black_neighbor_count == 2:
                new_black_tiles.add(l)

            x += 1
        y += 1

    return new_black_tiles


def get_tile_location(tile):
    i = 0
    l = 0 + 0j
    while i < len(tile):
        if tile[i] == 'e':
            l += 1
            i += 1
        elif tile[i] == 'w':
            l -= 1
            i += 1
        else:
            l += 1j if tile[i] == 'n' else -1j
            if tile[i + 1] == 'e':
                l += 0.5
            else:
                l -= 0.5
            i += 2

    return l


with open('input.txt', 'r') as f:
    tiles = [
        t.split('\n')[0] for t in f.readlines()
    ]

locations = [
    get_tile_location(tile) for tile in tiles
]

# Part 1
c = Counter(locations)

black_tiles = [
    t if n % 2 == 1 else None
    for t, n in c.items()
]

black_tiles = set(filter(lambda x: x is not None, black_tiles))
print(len(black_tiles))

# Part 2
NUMBER_OF_FLIPS = 100

for _ in range(NUMBER_OF_FLIPS):
    black_tiles = flip_tiles(black_tiles)

print(len(black_tiles))
