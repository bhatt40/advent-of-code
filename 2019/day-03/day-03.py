def get_coordinate_set_from_path(starting_coordinate, path):
    current_coordinate = starting_coordinate
    current_distance = 0
    coordinate_set = {current_coordinate}
    coordinate_distance_dict = {}
    for move in path:
        move_direction = move[0]
        move_distance = int(move[1:])
        if move_direction == 'U':
            new_coordinates = list(
                map(lambda x: (current_coordinate[0], current_coordinate[1] + x), range(1, move_distance + 1))
            )
            current_coordinate = [current_coordinate[0], current_coordinate[1] + move_distance]
        elif move_direction == 'D':
            new_coordinates = list(
                map(lambda x: (current_coordinate[0], current_coordinate[1] - x), range(1, move_distance + 1))
            )
            current_coordinate = [current_coordinate[0], current_coordinate[1] - move_distance]
        elif move_direction == 'L':
            new_coordinates = list(
                map(lambda x: (current_coordinate[0] - x, current_coordinate[1]), range(1, move_distance + 1))
            )
            current_coordinate = [current_coordinate[0] - move_distance, current_coordinate[1]]
        elif move_direction == 'R':
            new_coordinates = list(
                map(lambda x: (current_coordinate[0] + x, current_coordinate[1]), range(1, move_distance + 1))
            )
            current_coordinate = [current_coordinate[0] + move_distance, current_coordinate[1]]

        for index, coordinate in enumerate(new_coordinates):
            coordinate_distance_dict[coordinate] = current_distance + (index + 1)

        coordinate_set.update(new_coordinates)
        current_distance += move_distance

    coordinate_set.remove((0, 0))
    return coordinate_set, coordinate_distance_dict


def calculate_manhattan_distance(coordinate_a, coordinate_b):
    return abs(coordinate_a[0] - coordinate_b[0]) + abs(coordinate_a[1] - coordinate_b[1])


def calculate_step_distance(coordinate, distance_dict_a, distance_dict_b):
    return distance_dict_a[coordinate] + distance_dict_b[coordinate]


with open('input.txt', 'r') as f:
    wire_a_path = f.readline().split(',')
    wire_b_path = f.readline().split(',')

STARTING_COORDINATE = (0, 0)

wire_a_coordinate_set, wire_a_coordinate_distance_dict = get_coordinate_set_from_path(STARTING_COORDINATE, wire_a_path)
wire_b_coordinate_set, wire_b_coordinate_distance_dict = get_coordinate_set_from_path(STARTING_COORDINATE, wire_b_path)

intersections = wire_a_coordinate_set.intersection(wire_b_coordinate_set)

# Part 1
intersection_manhattan_distances = map(lambda x: calculate_manhattan_distance(STARTING_COORDINATE, x), intersections)

print(min(intersection_manhattan_distances))

# Part 2
intersection_step_distances = map(
    lambda x: calculate_step_distance(x, wire_a_coordinate_distance_dict, wire_b_coordinate_distance_dict),
    intersections
)

print(min(intersection_step_distances))





