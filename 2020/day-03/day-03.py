import functools


def get_new_location(starting_location, slope, field_width):
    column = (starting_location[0] + slope[0]) % field_width
    row = starting_location[1] + slope[1]

    return [column, row]


def get_tree_collisions_for_slope(slope):
    location = [0, 0]
    count = 0
    while location[1] < len(field):
        if field[location[1]][location[0]] == '#':
            count += 1
        location = get_new_location(location, slope, len(field[0]) - 1)

    return count


with open('input.txt', 'r') as f:
    field = f.readlines()

# Part 1
tree_collisions = get_tree_collisions_for_slope((3, 1))
print(tree_collisions)


# Part 2
slopes = (
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
)

tree_collisions = map(get_tree_collisions_for_slope, slopes)
product = functools.reduce(lambda a, b: a*b, tree_collisions)

print(product)
